import os
import random
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio import connect
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration


class FileTransferQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flows = {}

    def create_flow(self, flow_id: int, file_path: str):
        if flow_id in self.flows:
            raise ValueError("Flow ID already exists")
        self.flows[flow_id] = file_path

    async def send_file(self, flow_id: int):
        if flow_id not in self.flows:
            raise ValueError("Flow ID not found")

        file_path = self.flows[flow_id]
        file_size = os.path.getsize(file_path)

        with open(file_path, 'rb') as file:
            offset = 0
            while offset < file_size:
                packet_size = random.randint(1000, 2000)
                chunk = file.read(packet_size)
                if not chunk:
                    break
                stream_id = self._get_next_available_stream_id()
                self._send_stream_data(flow_id, stream_id, chunk)
                offset += packet_size

    def _get_next_available_stream_id(self):
        # Implement a method to get the next available stream ID
        return self._quic.get_next_available_stream_id()

    def _send_stream_data(self, flow_id, stream_id, data):
        self._quic.send_stream_data(stream_id, data)


async def create_quic_client(host, port, quic_config):
    async with connect(host, port, configuration=quic_config, create_protocol=FileTransferQuicProtocol) as protocol:
        return protocol


async def create_quic_server(host, port, quic_config):
    return await serve(host, port, configuration=quic_config, create_protocol=FileTransferQuicProtocol)
