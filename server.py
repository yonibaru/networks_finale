import asyncio
from quic import create_quic_server
from aioquic.quic.configuration import QuicConfiguration


async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    server = await create_quic_server('localhost', 4433, config)

    print("Server running on localhost:4433")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
