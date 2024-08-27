import socket
import threading
import random
import os

BUFFER_SIZE = 64  # Size of the buffer for receiving data
HEADER_SIZE = 256 

def create_header(filepath):
    file_name = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)
    header = f"{file_name}:{file_size}".encode('utf-8')
    header += b' ' * (256 - len(header))  # Padding to ensure header is 256 bytes
    return header

def send_file(filepath, client_socket):
    with open(filepath, 'rb') as f:
        header = create_header(filepath)
        print(f"header={header}")
        client_socket.sendall(header)  # At first, send the header 
        packet_size = random.randint(1000, 2000)
        while True:
            data = f.read(packet_size)
            if not data:
                break
            client_socket.sendall(data)
    print(f"Finished sending {filepath}")
    

def serve_client(client_socket, files_to_send):
    print(f"Handling client {client_socket.getpeername()}")

    streams = []
    for i in range(len(files_to_send)):
        file = files_to_send[i]
        # Create a thread (stream) for each file to send
        streams.append(threading.Thread(target=send_file, args=(file, client_socket)))
    
    # Start all threads
    for stream in streams:
        stream.start()
        stream.join()

    # Wait for all threads to finish
    # for stream in streams:

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
            serve_client(client_socket,files_to_send)
            # cl4ient_thread = threading.Thread(target=serve_client, args=(client_socket, files_to_send))
            # client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    host = 'localhost'
    port = 9996
    files = ["file1.txt", "file2.txt", "file3.txt"]  # Assume these are the files available in the server directory
    start_server(host, port, files)
