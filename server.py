import socket
import threading
from quic import handle_server


def server_main(host, port, file_to_send):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_server,
                         args=(conn, file_to_send)).start()


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    file_to_send = 'file_to_send.txt'
    server_main(host, port, file_to_send)
