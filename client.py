import socket

BUFFER_SIZE = 4096 
HEADER_SIZE = 256 # header is a fixed 256 bytes, accommodating the file name and file size

def request_all_files(connection):
    # Client continuously requests the next file in "queue", if such exists
    while True:
        if not request_file(connection):
            print("All files receieved. Closing connection.")
            break

def request_file(connection):
    # First receive the header length and format it
    header = connection.recv(HEADER_SIZE).decode('utf-8').strip()
    
    # Check if there is no more data coming from the server
    if not header:
        return False  # No more files to receive
    
    file_name, file_size_str = header.split(':')
    file_size = int(file_size_str)
     
    # ! Notice a file sent as "file1.txt" is saved as "new_file1.txt" just so files won't override eachother since they are in the same directory.
    with open("new_" + file_name, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            remaining = file_size - bytes_received
            frame = connection.recv(min(BUFFER_SIZE, remaining))
            if not frame:
                break
            f.write(frame)
            bytes_received += len(frame)
    
    print(f"Successfully received file: {file_name}, size: {file_size} bytes")
    return True

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket

# For simplicity's sake, arguments are provided here
if __name__ == "__main__":
    host = 'localhost'
    port = 9994
    connection = connect_to_server(host, port)
    request_all_files(connection)
