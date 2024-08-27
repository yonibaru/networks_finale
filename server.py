import socket
import threading

def send_file(self, filepath):
        with open(filepath, 'rb') as f:
            packet_size = random.randint(1000, 2000)
            while True:
                data = f.read(packet_size)
                if not data:
                    break
                self.connection.sendall(data)


def start_server(host, port, files_to_send):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10) # 10 users maximum

    print(f"Server listening on {host}:{port}")


    while True:
        client_sock, addr = server_socket.accept()
        print(f"Connection from {addr}")

        threads = []
        for file in files_to_send:
            threads.append(threading.Thread(target=send_file,args=(client_sock, file)))
        
        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        client_sock.close()



if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    files = ["file1.txt","file2.txt","file3.txt"] # Assume these are the files availible in the server directory
    start_server(host, port, files)
