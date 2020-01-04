import asyncio
import socket
import logging
import colorlog

from typing import Tuple, Optional, Dict


class SocketReceiver:
    def __init__(self,
                 host: str = "0.0.0.0",
                 port: int = 8080,
                 loop=None):
        self.host = host
        self.port = port

        self.sock: Optional[socket.socket] = None

        self.hosts: Dict[str, dict] = {}
        self.socks: Dict[socket.socket, Tuple[str, int]] = dict()

        self.loop = loop or asyncio.get_event_loop()

        # logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s][%(levelname)s %(filename)s:%(lineno)d] %(message)s%(reset)s",
            log_colors={
                "INFO": "green",
                "WARN": "yellow",
                "EXCEPTION": "red",
                "ERROR": "red",
                "CRITICAL": "red",
                "NOTSET": "white",
                "DEBUG": "white"
            },
            style="%"
        ))
        self.logger.addHandler(console_handler)

    @property
    def addr(self) -> Tuple[str, int]:
        return self.host, self.port

    def run(self):
        self.loop.run_until_complete(self._run())

    async def _run(self):
        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(8)
        self.sock.setblocking(False)

        while True:
            c_sock, c_addr = await self.loop.sock_accept(self.sock)
            self.socks[c_sock] = c_addr
            self.loop.create_task(self.handler(c_sock, c_addr))

    async def handler(self, c_sock: socket.socket, c_addr: Tuple[str, int]):
        msg = await self.recv(c_sock)  # Expect R:hostname

        if not msg.startswith("R"):
            return await self.destroy(c_sock, c_addr)

        _, hostname = msg.split(":", 1)

        if hostname in self.hosts:  # If duplicated hostname
            await self.sendall(c_sock, "E:Dup")
            return await self.destroy(c_sock, c_addr)

        self.hosts[hostname] = {
            "IP": c_addr[0],
            "Port": c_addr[1],
        }

        await self.sendall(c_sock, "S:OK")

        msg = await self.recv(c_sock)  # Except C:

        mode, *payload = msg.split(":", 1)

        if mode != "C":
            await self.sendall(c_sock, "E:Nah")
            return await self.destroy(c_sock, c_addr)

        assert mode, "C"

        while True:
            msg = await self.recv(c_sock)
            mode, *data = msg.split(":", 1)

    async def recv(self, sock: socket.socket, size: int = 2**12) -> str:
        payload = None
        while not payload:
            payload = await self.loop.sock_recv(sock, size)

        msg: str = payload.decode()
        ip, _ = self.socks.get(sock, ('256.256.256.256', 0))
        self.logger.debug("S <- C {:>15}: {}".format(ip, msg))

        return msg

    async def sendall(self, sock: socket.socket, data: str) -> int:
        ip, _ = self.socks.get(sock, ('256.256.256.256', 0))
        self.logger.debug("S -> C {:>15}: {}".format(ip, data))
        return await self.loop.sock_sendall(sock, data.encode())

    async def destroy(self, c_sock: socket.socket, c_addr: Tuple[str, int]):
        ip, port = c_addr

        if ip in self.hosts:
            del self.hosts[ip]

        return c_sock.close()
