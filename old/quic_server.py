import socket
import random
import threading
import time

# Constants
MIN_PACKET_SIZE = 1000
MAX_PACKET_SIZE = 2000
BUFFER_SIZE = 4096 # Size of the buffer for receiving data

class Flow:
    def __init__(self, flow_id, file_path):
        self.flow_id = flow_id
        self.file_path = file_path
        self.file_size = self.get_file_size()
        self.sent_bytes = 0
        self.closed = False
        self.packet_size = random.randint(MIN_PACKET_SIZE, MAX_PACKET_SIZE)

    def get_file_size(self):
        with open(self.file_path, 'rb') as f:
            f.seek(0, 2)
            return f.tell()

class QUICConnection:
    def __init__(self, address):
        self.address = address
        self.flows = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(address)
        self.lock = threading.Lock()

    def handle_packet(self, data, addr):
        try:
            decoded_data = data.decode()
            print(f"Received data: {decoded_data}")

            # Split based on the first colon to separate header from data
            data_arr = decoded_data.split(":", 2)
            flow_id = int(data_arr[0])
            packet_size = int(data_arr[1])
            packet_data = data_arr[2]
            print(f"Handling packet: flow_id={flow_id}, packet_size={packet_size}")

            # Ensure that the data length matches the expected packet size
            if len(packet_data) != packet_size:
                print(f"Warning: Packet size mismatch. Expected {packet_size}, got {len(packet_data)}.")

            with self.lock:
                if flow_id in self.flows:
                    print("BLA BLA")
                    flow = self.flows[flow_id]
                    flow.sent_bytes += len(packet_data)
                    if flow.sent_bytes >= flow.file_size:
                        flow.closed = True
                        print(f"Flow {flow_id} completed from {addr}.")
            
            print("DONE!")

        except ValueError as e:
            print(f"Error parsing packet data: {e}. Received data: {data}")
        except Exception as e:
            print(f"Unexpected error: {e}. Received data: {data}")

    def receive(self):
        while True:
            data, addr = self.socket.recvfrom(BUFFER_SIZE)
            self.handle_packet(data, addr)

    def close(self):
        self.socket.close()

def main_server():
    server_address = ("localhost", 9989)
    connection = QUICConnection(server_address)

    # Start a thread to receive packets
    threading.Thread(target=connection.receive).start()

    # Keep the server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        connection.close()

if __name__ == "__main__":
    main_server()

