import socket

BUFFER_SIZE = 4096 # Size of the buffer for receiving data

def request_all_files(connection):
    # Client continuously requests the next file in queue
    while True:
        if not request_file(connection):
            print("No more files to receive. Closing connection.")
            break

def request_file(connection):
    # First receive the header length (4 bytes)
    header_length_data = connection.recv(4)
    
    # Check if there is no more data coming from the server
    if not header_length_data:
        return False  # No more files to receive

    # First receive the header length (4 bytes)
    header_length = int.from_bytes(connection.recv(4), 'big')
    
    # Now receive the actual header based on its length
    header = connection.recv(header_length).decode('utf-8')
    file_name, file_size_str = header.split(':')
    file_size = int(file_size_str)
    # Prepare to receive the file content
    with open("new_" + file_name, 'wb') as f:
        bytes_received = 0
    
        while bytes_received < file_size:
            frame = connection.recv(BUFFER_SIZE)
            if not frame:
                break
                # await reconnect else fail sending failed: not all data has been received
            f.write(frame)
            bytes_received += len(frame)
    
    print(f"Received file: {file_name}, size: {file_size} bytes")
    return True

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket

# For simplicity's sake, arguments are provided here
if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    connection = connect_to_server(host, port)
    request_all_files(connection)
