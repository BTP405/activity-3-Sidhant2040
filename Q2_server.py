import socket
import pickle
import threading
from queue import Queue

class TaskQueueServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.worker_queue = Queue()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Connection established from {addr}")

                threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, connection):
        with connection:
            try:
                task_data = b""
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    task_data += data

                task = pickle.loads(task_data)
                self.worker_queue.put((task, connection))
            except pickle.PickleError as e:
                print(f"Pickle error: {e}")

    def distribute_tasks(self):
        while True:
            task, connection = self.worker_queue.get()
            worker_thread = threading.Thread(target=self.execute_task, args=(task, connection))
            worker_thread.start()

    def execute_task(self, task, connection):
        task_function = task['function']
        args = task['args']
        kwargs = task['kwargs']
        try:
            result = task_function(*args, **kwargs)
            pickled_result = pickle.dumps(result)
            connection.sendall(pickled_result)
        except Exception as e:
            print(f"Error executing task: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    server = TaskQueueServer('localhost', 5555)

    # Start the task distribution thread
    threading.Thread(target=server.distribute_tasks).start()

    # Start the server
    server.start_server()
