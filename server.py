import socket
import threading
import random
import os

MAX_CLIENTS = 10
FILENAME_LENGTH = 32
PACKET_ID_LENGTH = 7
PACKET_SIZE_LENGTH = 4
HEADER_SIZE = FILENAME_LENGTH + PACKET_ID_LENGTH + PACKET_SIZE_LENGTH

'''
Creates an appropriate header that would be sent along with the packet data to the client.
Headers are of the following format:
file_name:frame_id:packet_size:file_data
    /\       /\        /\         
     |        |         |
32 bytes   7 bytes     4 bytes

TOTAL SIZE: 43 BYTES (Without the :)

'''
def inject_file_data(filepath, data, id, packet_size):
    # Inject the file path, data id, packet size, and data into the data
    # Conceptually, this is equivilant to creating a header.
    if not data:
        return None
    
    # .zfill pads a string with 0's until the desired length is reached
    # .ljust pads a string with whitespaces (" ") until the desired length is reached
    formatted_filename = filepath[:FILENAME_LENGTH].ljust(FILENAME_LENGTH)
    formatted_packet_id = str(id).zfill(PACKET_ID_LENGTH)[:PACKET_ID_LENGTH]
    formatted_packet_size = str(packet_size).zfill(PACKET_SIZE_LENGTH)[:PACKET_SIZE_LENGTH]
    
    # Form a 43-byte header
    formatted_header = (f"{formatted_filename}{formatted_packet_id}{formatted_packet_size}")
    # print(f"formatted_header={formatted_header} size={len(formatted_header)}")
    # print(f"formatted_filename={formatted_filename} size={len(formatted_filename)}")
    # print(f"formatted_packet_id={formatted_packet_id} size={len(formatted_packet_id)}")
    # print(f"formatted_packet_size={formatted_packet_size} size={len(formatted_packet_size)}")
    
    if len(formatted_header) != HEADER_SIZE:
        raise ValueError(f"Header size is not of the required {HEADER_SIZE} bytes. Current size: {len(formatted_header)}")
    
    return f"{formatted_header}{data}"

'''
This function sends a file to a client socket
'''
def send_file(filepath, client_socket):
    total_bytes_sent = 0
    packet_count = 0

    with open(filepath, 'rb') as f:
        packet_size = random.randint(1000, 2000)  # Random packet size
        counter = 1  # Data ID - to keep track of the order of the data
        while True:
            original_data = f.read(packet_size).decode('utf-8')  # Read data from file

            # If the data is less than the packet size, adjust the packet size.
            if len(original_data) < packet_size:
                if not original_data:
                    break
                packet_size = len(original_data)

            # Inject the file data into the original data
            formatted_data = inject_file_data(filepath, original_data, counter, packet_size).encode('utf-8')
            if not formatted_data or len(formatted_data) == 0:
                break
            # print("### SENT FRAME: ###")
            # print(f"{injected_data}")
            # Send the injected data to the client
            client_socket.sendall(formatted_data)
            total_bytes_sent += len(formatted_data)
            packet_count += 1
            counter += 1

    print(f"Finished sending {filepath}")


'''
Each client is served by the means of sending the entire directory of txt files that exist in the server.
'''
def serve_client(client_socket, files_to_send):
    print(f"Handling client {client_socket.getpeername()}")

    streams = []  # List of threads (streams) for each file to send
    for i in range(len(files_to_send)):            
        file = files_to_send[i]
        if not os.path.isfile(file):
            print(f"{file} is missing from the server directory and will not be sent to the client. Continuing...")
            continue
        # Create a thread (stream) for each file to send
        streams.append(threading.Thread(target=send_file, args=(file, client_socket)))

    # Run all threads (streams) to send the files
    for stream in streams:
        stream.start()

    # Ensures that the main thread waits for all the threads (streams) to complete their execution before proceeding.
    for stream in streams:
        stream.join()

    print(f"All files sent to client {client_socket.getpeername()}")
    client_socket.close()  # Close connection after sending all files


'''
Initalizing the server and listening for clients.
'''
def start_server(host, port, files_to_send):
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # Create a server socket
    server_socket.bind((host, port))
    server_socket.listen(MAX_CLIENTS)  # Up to 10 clients can connect

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()  # Accept incoming connection
            print(f"Connection from {addr}")

            # Handle the client, send files
            serve_client(client_socket, files_to_send)
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    host = 'localhost'
    port = 3006
    # The files that would be sent to each client (if any are missing from the server directory they would be skipped)
    files = ["file1.txt","file2.txt","file3.txt","file4.txt","file5.txt","file6.txt","file7.txt","file8.txt","file9.txt","file10.txt"]
    start_server(host, port, files)
