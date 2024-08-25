import socket
from QUIC import QUICConnection


def receive_file(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    quic_conn = QUICConnection(client_socket)
    file_data = quic_conn.receive_data()
    # Print first 100 bytes for brevity
    print(f'Received file data: {file_data[:100]}...')
    quic_conn.close()


if __name__ == '__main__':
    receive_file()
