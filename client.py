import socket
import time

BUFFER_SIZE = 256
packets_sent = 0
bytes_sent = 0
total_packets_sent_time = 0

'''
Save the file data to the file. The file data is saved to the file with the name "new_" + file_name.
The data is saved in a hashmap with the file name as the key and the data ID as the value.

Example:
files_dict = {
    "file1.txt": {
        1: "data1",
        2: "data2",
        ...
    },
    "file2.txt": {
        1: "data1",
        2: "data2",
        ...
    },
    ...
}
'''


def request_all_files(connection):
    while True:
        files_dict = {}  # Dictionary to store the files and file data

        # Accept the file data from the server, keep accepting until there is no more data
        file_received = request_file(connection, files_dict)
        while file_received:
            file_received = request_file(connection, files_dict)

        # Save the file data to the file, ordered by the data ID
        for file_name in files_dict:
            with open("new_" + file_name, 'wb') as f:
                for data_id in sorted(files_dict[file_name]):
                    f.write(files_dict[file_name][data_id].encode('utf-8'))
        print("--- File Transfer Complete ---")
        print(f"Bytes Sent: {bytes_sent}")
        print(f"Packets Sent: {packets_sent}")
        print(
            f"Average bytes per second: {bytes_sent / total_packets_sent_time}")
        print(
            f"Average packets per second: {packets_sent / total_packets_sent_time}")
        print("------------------------------")
        break


'''
Request the file data from the server. The file data is received from the server and saved to the files_dict.
The file data is received in the format "file_name:data_id:packet_size:data".
'''


def request_file(connection, files_dict):
    global packets_sent, bytes_sent, total_packets_sent_time

    # Start time to measure the time taken to receive all files
    start_time = time.time()

    # Receive the file data from the server
    frame = connection.recv(BUFFER_SIZE).decode(
        'utf-8')

    # If there is no data, the client has received all the data
    if not frame:
        return False

    # Split the data into file name, data id, packet size, and data
    file_name, data_id, packet_size, data = frame.split(':', 3)

    data_id = int(data_id)
    packet_size = int(packet_size)

    # If the data is less than the packet size, adjust the packet size
    if len(data) < packet_size:
        data += connection.recv(packet_size - len(data)).decode('utf-8')

    end_time = time.time()
    duration = end_time - start_time
    packets_sent += 1
    bytes_sent += len(data)
    total_packets_sent_time += duration

    print(f"Time taken to receive packet: {duration}")

    # Save the file data to the files_dict
    if file_name not in files_dict:
        files_dict[file_name] = {data_id: data}
    else:
        files_dict[file_name][data_id] = data

    return True


'''
Connect to the server. The client will connect to the server using the host and port provided.
'''


def connect_to_server(host, port):
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket


# For simplicity's sake, arguments are provided here
if __name__ == "__main__":
    host = 'localhost'
    port = 3000
    connection = connect_to_server(host, port)
    request_all_files(connection)
