import socket
from QUIC import QUICConnection


def handle_client(conn):
    quic_conn = QUICConnection(conn)
    # Simulate sending a file
    file_data = b'This is the content of the file.' * 100  # Example file data
    quic_conn.send_data(file_data)
    quic_conn.close()


def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Server listening on {host}:{port}')

    while True:
        conn, addr = server_socket.accept()
        print(f'Connection from {addr}')
        handle_client(conn)


if __name__ == '__main__':
    start_server()
