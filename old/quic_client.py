import socket
import threading
import os
import random
import time

MIN_PACKET_SIZE = 1000
MAX_PACKET_SIZE = 2000

class QUICClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_file(self, file_path, flow_id):
        file_size = os.path.getsize(file_path)
        sent_bytes = 0

        with open(file_path, 'rb') as f:
            while sent_bytes < file_size:
                packet_size = random.randint(MIN_PACKET_SIZE, MAX_PACKET_SIZE)
                data = f.read(packet_size)
                if not data:
                    break
                # Format: "flow_id:packet_size:data"
                packet_header = f"{flow_id}:{len(data)}".encode()
                self.socket.sendto(packet_header + b':' + data, self.server_address)
                sent_bytes += len(data)
                time.sleep(0.01)  # Simulate network delay
                print(f"Sent packet: flow_id={flow_id}, packet_size={len(data)}, data={data}")
        print(f"File {file_path} sent successfully.")

    def close(self):
        self.socket.close()

def main_client():
    server_address = ("localhost", 9989)
    client = QUICClient(server_address)

    # Send multiple files
    threading.Thread(target=client.send_file, args=("file1.txt", 1)).start()
    threading.Thread(target=client.send_file, args=("file2.txt", 2)).start()
    threading.Thread(target=client.send_file, args=("file3.txt", 3)).start()

    # Wait for a bit before closing
    time.sleep(5)
    client.close()

if __name__ == "__main__":
    main_client()

