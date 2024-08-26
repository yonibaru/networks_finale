import socket
import threading
import random
import os


class QUICProtocol:
    def __init__(self, connection):
        self.connection = connection

    def send_file(self, filepath):
        with open(filepath, 'rb') as f:
            packet_size = random.randint(1000, 2000)
            while True:
                data = f.read(packet_size)
                if not data:
                    break
                self.connection.sendall(data)

    def receive_file(self, filepath):
        with open(filepath, 'wb') as f:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                f.write(data)


def handle_client(connection):
    quic = QUICProtocol(connection)
    quic.receive_file('received_file.txt')
    connection.close()


def handle_server(connection, file_to_send):
    quic = QUICProtocol(connection)
    quic.send_file(file_to_send)
    connection.close()
