import socket
import pickle

class TaskQueueClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def send_task(self, task_function, *args, **kwargs):
        task_data = {
            'function': task_function,
            'args': args,
            'kwargs': kwargs
        }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_host, self.server_port))
            pickled_task = pickle.dumps(task_data)
            client_socket.sendall(pickled_task)

            result_data = client_socket.recv(1024)
            result = pickle.loads(result_data)
            print(f"Result from server: {result}")

if __name__ == "__main__":
    client = TaskQueueClient('localhost', 5555)

    # Example task: a simple function to add two numbers
    def add_numbers(x, y):
        return x + y

    # Send the task to the server
    client.send_task(add_numbers, 3, 4)
