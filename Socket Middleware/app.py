import asyncio
import logging
import colorlog
from datetime import datetime

from typing import Tuple


class SocketReceiver:
    def __init__(self,
                 host: str = "0.0.0.0",
                 port: int = 8080):
        self.host = host
        self.port = port

        self.sessions: dict = {}

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

    async def handle_echo(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            addr = writer.get_extra_info('peername')

            data = await self.read(reader, writer)
            message = data.decode()
            mode, device_id = message.split(":", 1)

            if mode != "R":
                return await self.write(reader, writer, b"E:Mod")

            self.logger.warning(f"Host {device_id}: Register requested")

            await self.write(reader, writer, b"S:OK")
            await writer.drain()

            data = await self.read(reader, writer)
            message = data.decode()
            try:
                mode, device_id, location = message.split(":", 2)
                lon, lat = map(float, location.split(",", 1))
                self.logger.warning(f"Host {device_id}: Registered at {lon}, {lat}")

                self.sessions[device_id] = {
                    "GPS": (lon, lat, ),
                    "Address": addr,
                    "Registered": datetime.now().timestamp()
                }

                await self.write(reader, writer, b"S:OK")
                await writer.drain()

                self.logger.info(f"Clse {addr!r}")
                writer.close()
            except ValueError:  # unpacking not matched
                return await self.write(reader, writer, b"E:Val")
            except TypeError:  # cannot unpack
                return await self.write(reader, writer, b"E:Tpe")

            # TODO: Report to Backend
        except:
            return await self.write(reader, writer, b"E:Unk")

    async def read(self, reader, writer, size: int = 2**12) -> bytes:
        data = await reader.read(size)
        self.logger.info(f"Recv {writer.get_extra_info('peername')!r}: {data!r}")
        return data

    async def write(self, reader, writer, data: bytes):
        ret = writer.write(data + b"\r\n")
        self.logger.info(f"Send {writer.get_extra_info('peername')!r}: {data!r}")
        return ret

    async def main(self):
        server = await asyncio.start_server(
            self.handle_echo, self.host, self.port)
    
        addr = server.sockets[0].getsockname()
        self.logger.info(f'Serving on {addr}')
    
        async with server:
            await server.serve_forever()

    def run(self):
        asyncio.run(self.main())

