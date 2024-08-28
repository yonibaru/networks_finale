import socket

BUFFER_SIZE = 256


def request_all_files(connection):
    # Client continuously requests the next file in "queue", if such exists
    while True:
        files_dict = {}

        file_received = request_file(connection, files_dict)
        while file_received:
            file_received = request_file(connection, files_dict)

        for file_name in files_dict:
            with open("new_" + file_name, 'wb') as f:
                for data_id in sorted(files_dict[file_name]):
                    f.write(files_dict[file_name][data_id])


def request_file(connection, files_dict):
    frame = connection.recv(BUFFER_SIZE).decode('utf-8')

    if not frame:
        return False

    print(f"👽Received frame👽: {frame}")
    file_name, data_id, packet_size, data = frame.split(':', 3)
    data_id = int(data_id)
    packet_size = int(packet_size)
    if len(data) < packet_size:
        data += connection.recv(packet_size - len(data)).decode('utf-8')
    print(f"Received file: {file_name}, data_id: {data_id}")

    if file_name not in files_dict:
        files_dict[file_name] = {data_id: data}
    else:
        files_dict[file_name][data_id] = data

    # ! Notice a file sent as "file1.txt" is saved as "new_file1.txt" just so files won't override eachother since they are in the same directory.
    # with open("new_" + file_name, 'wb') as f:
    #     bytes_received = 0
    #     while bytes_received < file_size:
    #         remaining = file_size - bytes_received
    #         frame = connection.recv(min(BUFFER_SIZE, remaining))
    #         if not frame:
    #             break
    #         f.write(frame)
    #         bytes_received += len(frame)

    # print(f"Successfully received file: {file_name}, size: {file_size} bytes")
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
