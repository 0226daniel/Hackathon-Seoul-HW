import asyncio

from typing import Tuple


class SocketReceiver:
    def __init__(self,
                 host: str = "0.0.0.0",
                 port: int = 8080):
        self.host = host
        self.port = port

    @property
    def addr(self) -> Tuple[str, int]:
        return self.host, self.port
