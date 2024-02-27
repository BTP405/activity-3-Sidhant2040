import socket
import pickle
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            # Thread to handle new client connections
            threading.Thread(target=self.accept_clients, daemon=True).start()

            while True:
                pass  # Main thread continues to handle messages from clients

    def accept_clients(self):
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection established from {addr}")

            with self.lock:
                self.clients.append(conn)

            # Thread to handle messages from the new client
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                # Unpickle the message
                message = pickle.loads(data)

                # Broadcast the message to all clients
                self.broadcast(message, client_socket)

            except pickle.PickleError as e:
                print(f"Pickle error: {e}")
                break
            except Exception as e:
                print(f"Error handling client: {e}")
                break

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                # Avoid sending the message back to the sender
                if client != sender_socket:
                    try:
                        # Pickle and send the message
                        pickled_message = pickle.dumps(message)
                        client.sendall(pickled_message)
                    except Exception as e:
                        print(f"Error broadcasting message: {e}")

if __name__ == "__main__":
    server = ChatServer('localhost', 5555)
    server.start_server()
