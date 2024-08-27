import socket

BUFFER_SIZE = 64 # Size of the buffer for receiving data
HEADER_SIZE = 264 # 8 bytes for file_size, and 256 bytes for file_name

def request_all_files(connection):
    # Client continuously requests the next file in queue
    while True:
        if not request_file(connection):
            print("No more files to receive. Closing connection.")
            break

def request_file(connection):
    # First receive the header length (4 bytes)
    header = connection.recv(HEADER_SIZE).decode('utf-8').strip()
    
    # Check if there is no more data coming from the server
    if not header:
        return False  # No more files to receive
    
    print(f"header={header}") 
    file_name, file_size_str = header.split(':')
    file_size = int(file_size_str)
    # Prepare to receive the file content
    with open("new_" + file_name, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            frame = connection.recv(BUFFER_SIZE)
            if not frame:
                break
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
    port = 9996
    connection = connect_to_server(host, port)
    request_all_files(connection)
