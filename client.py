import socket
import random

BUFFER_SIZE = 4096 # Size of the buffer for receiving data
FILE_END_MARKER = b"<END_OF_FILE>"  # Marker to signify the end of a file

def request_files(connection, files):
    try:
        for file in files:
            get_file(file,connection)
        print("Successfully received all files.")
    finally:
        connection.close()
        print("Connection with the server has closed.")


def get_file(filepath, connection):
    with open(filepath, 'wb') as f:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if FILE_END_MARKER in data:
                # Split data at the marker to save the file and ignore the marker
                file_data, remaining_data = data.split(FILE_END_MARKER,1)
                f.write(file_data)
                break
            else:
                f.write(data)

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket

# For simplicity's sake, arguments are provided here
if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    files = ["received_file1.txt", "received_file2.txt", "received_file3.txt"]  # Names for the files to save received data
    # Files the user would like to download from the server
    connection = connect_to_server(host, port)
    request_files(connection,files)
