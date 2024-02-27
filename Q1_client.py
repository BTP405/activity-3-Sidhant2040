import socket
import pickle

def send_file(file_path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        try:
            with open(file_path, 'rb') as file:
                filename = file.name.split("/")[-1]
                content = file.read()
                file_object = {'filename': filename, 'content': content}
                pickled_file = pickle.dumps(file_object)
                client_socket.sendall(pickled_file)
                print("File sent successfully.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    send_file('test.txt', 'localhost', 5555)
