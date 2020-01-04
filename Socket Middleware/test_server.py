import asyncio


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    writer.write(b"S:OK")
    print(f"Send: {message!r}")
    await writer.drain()

    data = await reader.read(2**12)
    message = data.decode()

    print(f"Received {message!r}")
    writer.write(b"S:OK")
    print(f"Send: {message!r}")
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8080)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
