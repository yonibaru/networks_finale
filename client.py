import socket
from quic import handle_client


def client_main(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to {host}:{port}")

    handle_client(client_socket)


if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    files = ["file1.txt","file3.txt"] # Files the user would like to download from the server
    client_main(host, port)
