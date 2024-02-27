import socket
import pickle

def receive_file(server_socket, save_directory):
    connection, addr = server_socket.accept()

    with connection:
        file_data = b""
        while True:
            data = connection.recv(1024)
            if not data:
                break
            file_data += data

        try:
            file_object = pickle.loads(file_data)
            save_path = f"{save_directory}/{file_object['filename']}"
            with open(save_path, 'wb') as file:
                file.write(file_object['content'])
            print("File received and saved successfully.")
        except pickle.PickleError as e:
            print(f"Pickle error: {e}")

def start_server(host, port, save_directory):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            receive_file(server_socket, save_directory)

if __name__ == "__main__":
    start_server('localhost', 5555, 'server_files')
