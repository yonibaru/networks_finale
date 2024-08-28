import socket
import threading
import random

BUFFER_SIZE = 256

'''
Add the file data to the data to be sent to the client. The file path, data id, packet size, and data are added to the data.
'''


def inject_file_data(filepath, data, id, packet_size):
    # Inject the file path, data id, packet size, and data into the data
    if not data:
        return None
    return f"{filepath}:{id}:{packet_size}:{data}".encode('utf-8')


'''
The server will send the file to the client. The server will read the file and send the file data to the client.
'''


def send_file(filepath, client_socket):
    with open(filepath, 'rb') as f:
        packet_size = random.randint(1000, 2000)  # Random packet size
        counter = 1  # Data ID - to keep track of the order of the data
        while True:
            original_data = f.read(packet_size).decode(
                'utf-8')  # Read data from file

            # If the data is less than the packet size, adjust the packet size.
            if len(original_data) < packet_size:
                if not original_data:
                    break
                packet_size = len(original_data)

            # Inject the file data into the original data
            injected_data = inject_file_data(
                filepath, original_data, counter, packet_size)
            if not injected_data:
                break

            # Send the injected data to the client
            client_socket.sendall(injected_data)
            counter += 1
    print(f"Finished sending {filepath}")


'''
The server will handle the client.
'''


def serve_client(client_socket, files_to_send):
    print(f"Handling client {client_socket.getpeername()}")

    streams = []  # List of threads (streams) for each file to send
    for i in range(len(files_to_send)):
        file = files_to_send[i]

        # Create a thread (stream) for each file to send
        streams.append(threading.Thread(
            target=send_file, args=(file, client_socket)))

    # Run all threads (streams) to send the files
    for stream in streams:
        stream.start()

    # Ensures that the main thread waits for all the threads (streams) to complete their execution before proceeding.
    for stream in streams:
        stream.join()

    print(f"All files sent to client {client_socket.getpeername()}")
    client_socket.close()  # Close connection after sending all files


'''
The server will start and listen for incoming connections from clients.
'''


def start_server(host, port, files_to_send):
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # Create a server socket
    server_socket.bind((host, port))
    server_socket.listen(10)  # Up to 10 clients can connect

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
    port = 3000
    # Assume these are the files available in the server directory
    files = ["file1.txt", "file2.txt", "file3.txt"]
    start_server(host, port, files)
