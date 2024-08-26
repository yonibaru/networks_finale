import asyncio
import random
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted

class MyQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files_to_transfer = []  # List of (file_path, stream_id)

    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            # Start multiple flows once the handshake is complete
            for file_path in self.files_to_transfer:
                self.start_flow(file_path)
                print("Sending File")

    def start_flow(self, file_path):
        # Open a new QUIC stream for each file transfer
        stream_id = self._quic.get_next_available_stream_id()
        self.files_to_transfer.append((file_path, stream_id))
        asyncio.ensure_future(self.send_file(file_path, stream_id)) #! What does this do?

    async def send_file(self, file_path, stream_id):
        try:
            with open(file_path, "rb") as f:
                packet_size = random.randint(1000, 2000)
                while True:
                    # Read random-sized chunks of the file
                    data = f.read(packet_size)
                    if not data:
                        break
                    # Send the data over the QUIC stream
                    self._quic.send_stream_data(stream_id, data)
                    await self.transmit() #! What does this do?
            # Finish the stream when file transfer is complete
            self._quic.send_stream_data(stream_id, b'', end_stream=True) #! What does this do?
            await self.transmit() #! What does this do?
        except FileNotFoundError:
            print(f"File not found: {file_path}")

async def main():
    configuration = QuicConfiguration(is_client=True) #! What does this do?
    # configuration.verify_mode = False
    # configuration.is_insecure = False
    # Example server address and port
    server_addr = 'localhost'
    server_port = 1234

    # Connect to the server
    async with connect(server_addr, server_port, configuration=configuration, create_protocol=MyQuicProtocol) as protocol:
        # List of files to transfer
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        
        # Add files to the protocol for transferring
        protocol.files_to_transfer.extend(files)
        
        # Keep the connection open until all files are transferred
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
