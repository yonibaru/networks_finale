import socket
import threading
import random
import os

BUFFER_SIZE = 4096 # Size of the buffer for receiving data

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
                data = self.connection.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)



def handle_client(connection, files_requested):
    quic = QUICProtocol(connection)
    for file in files_requested:
        quic.receive_file("r_" + file)
    # quic.receive_file('received_file.txt')
    # We need to loop over the files the user would like to download and 
    # send each of them individually in a different thread
    connection.close()


def handle_server(connection, file_to_send):
    quic = QUICProtocol(connection)
    quic.send_file(file_to_send)
    connection.close()
