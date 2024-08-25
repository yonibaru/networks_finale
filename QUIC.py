import random
import socket


class QUICConnection:
    def __init__(self, conn):
        self.conn = conn

    def send_data(self, data):
        packet_size = random.randint(1000, 2000)
        for i in range(0, len(data), packet_size):
            self.conn.send(data[i:i+packet_size])

    def receive_data(self):
        data = b''
        while True:
            packet = self.conn.recv(2000)
            if not packet:
                break
            data += packet
        return data

    def close(self):
        self.conn.close()
