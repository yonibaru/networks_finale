import socket
import threading
import random
import os

BUFFER_SIZE = 4096
HEADER_SIZE = 256  # header is a fixed 256 bytes, accommodating the file name and file size


def inject_file_data(filepath, data, id):
    # Inject the file name and id into the data
    return f"{filepath}:{id}:{data}"


def send_file(filepath, client_socket):
    with open(filepath, 'rb') as f:
        # Multiple threads cannot simultaneously run this code, allowing for some synchornization.
        packet_size = random.randint(1000, 1800)
        counter = 1
        while True:
            original_data = f.read(packet_size)
            injected_data = inject_file_data(filepath, original_data, counter)
            if not injected_data:
                break
            client_socket.sendall(injected_data)
            counter += 1
    print(f"Finished sending {filepath}")


def serve_client(client_socket, files_to_send):
    print(f"Handling client {client_socket.getpeername()}")

    streams = []
    for i in range(len(files_to_send)):
        file = files_to_send[i]
        # Create a thread (stream) for each file to send
        streams.append(threading.Thread(
            target=send_file, args=(file, client_socket)))

    # Start all threads
    for stream in streams:
        stream.start()

    # Wait for all threads to finish
    for stream in streams:
        stream.join()

    print(f"All files sent to client {client_socket.getpeername()}")
    client_socket.close()  # Close connection after sending all files


def start_server(host, port, files_to_send):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)  # Up to 10 clients can connect

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            serve_client(client_socket, files_to_send)
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    host = 'localhost'
    port = 9994
    # Assume these are the files available in the server directory
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
    start_server(host, port, files)
