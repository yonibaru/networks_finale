import socket
import threading
from quic import handle_server


def start_server(host, port, file_to_send):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10) # 10 users maximum

    print(f"Server listening on {host}:{port}")


    while True:
        sock, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_server,args=(sock, file_to_send)).start()


if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    files = ["file1.txt","file2.txt","file3.txt"] # Assume these are the files availible in the server directory
    start_server(host, port, files)
