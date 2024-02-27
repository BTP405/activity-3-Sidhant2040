import socket
import pickle
import threading

class ChatClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        self.client_socket.connect((self.server_host, self.server_port))

        # Thread to handle receiving messages from the server
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Thread to handle sending messages to the server
        threading.Thread(target=self.send_messages).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                # Unpickle the message and display it
                message = pickle.loads(data)
                print(message)

            except pickle.PickleError as e:
                print(f"Pickle error: {e}")
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        while True:
            message = input("Enter your message: ")
            try:
                # Pickle and send the message
                pickled_message = pickle.dumps(message)
                self.client_socket.sendall(pickled_message)
            except pickle.PickleError as e:
                print(f"Pickle error: {e}")
            except Exception as e:
                print(f"Error sending message: {e}")
                break

if __name__ == "__main__":
    client = ChatClient('localhost', 5555)
    client.start_client()
