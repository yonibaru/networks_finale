import socket
import random

BUFFER_SIZE = 4096 # Size of the buffer for receiving data

def request_file(filepath,connection):
    with open(filepath, 'wb') as f:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket

# For simplicity's sake, arguments are provided here
if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    # Files the user would like to download from the server
    connection = connect_to_server(host, port)
    connection.close()
