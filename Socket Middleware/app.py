import asyncio
import socket

from typing import Tuple, Optional


class SocketReceiver:
    def __init__(self,
                 host: str = "0.0.0.0",
                 port: int = 8080,
                 loop=None):
        self.host = host
        self.port = port

        self.sock: Optional[socket.socket] = None

        self.hosts = {}

        self.loop = loop or asyncio.get_event_loop()

    @property
    def addr(self) -> Tuple[str, int]:
        return self.host, self.port

    def run(self):
        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(8)
        self.sock.setblocking(False)

        while True:
            c_sock, c_addr = await self.loop.sock_accept(self.sock)
            self.loop.create_task(self.handler(c_sock, c_addr))

    async def handler(self, c_sock: socket.socket, c_addr: Tuple[str, int]):
        msg = (await self.loop.sock_recv(c_sock, 2**12)).decode()  # Expect R:hostname

        if not msg.startswith("R"):
            return await self.destroy(c_sock, c_addr)

        _, hostname = msg.split(":", 1)

        if hostname in self.hosts:  # If duplicated hostname
            await self.loop.sock_sendall(c_sock, "E:Dup".encode())
            return await self.destroy(c_sock, c_addr)

        self.hosts[hostname] = {
            "IP": c_addr[0],
            "Port": c_addr[1],
        }

        await self.loop.sock_sendall(c_sock, "S:OK".encode())

        msg = (await self.loop.sock_recv(c_sock, 2**12)).decode()  # Except C:

        mode, payload = msg.split(":", 1)

        if mode != "C":
            await self.loop.sock_sendall(c_sock, "E:Nah".encode())
            return await self.destroy(c_sock, c_addr)

        assert mode, "C"

        while True:
            mode, data = (await self.loop.sock_recv(c_sock, 2**12)).decode().split(":", 1)

    async def destroy(self, c_sock: socket.socket, c_addr: Tuple[str, int]):
        ip, port = c_addr

        if ip in self.hosts:
            del self.hosts[ip]

        return c_sock.close()
