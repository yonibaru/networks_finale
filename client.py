import asyncio
from quic import create_quic_client
from aioquic.quic.configuration import QuicConfiguration


async def main():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False  # This disables certificate verification for simplicity

    client = await create_quic_client('localhost', 4433, config)

    # Create a flow with a file
    flow_id = 1
    client.create_flow(flow_id, 'file_to_transfer.txt')

    # Send the file
    await client.send_file(flow_id)

if __name__ == '__main__':
    asyncio.run(main())
