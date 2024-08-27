import socket
import threading
import random

BUFFER_SIZE = 4096  # Size of the buffer for receiving data

def send_file(filepath, connection):
    with open(filepath, 'rb') as f:
        while True:
            packet_size = random.randint(1000, 2000)
            data = f.read(packet_size)
            if not data:
                break
            connection.sendall(data)
    print(f"Finished sending {filepath}")
    connection.close()  # Close connection after sending all files

def serve_client(client_socket, files_to_send):
    print(f"Handling client {client_socket.getpeername()}")
    for file in files_to_send:
        file_thread = threading.Thread(target=send_file, args=(file, client_socket))
        file_thread.start()
        file_thread.join()  # Wait for this file transfer to complete before starting the next
    print(f"All files sent to client {client_socket.getpeername()}")

def start_server(host, port, files_to_send):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)  # Up to 10 clients can connect

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=serve_client, args=(client_socket, files_to_send))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    files = ["file1.txt", "file2.txt", "file3.txt"]  # Assume these are the files available in the server directory
    start_server(host, port, files)
