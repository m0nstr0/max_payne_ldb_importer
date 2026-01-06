import struct
from dataclasses import dataclass


class MaxChunk:
    def __init__(self, chunk_id, chunk_version) -> None:
        self.chunk_id = chunk_id
        self.chunk_version = chunk_version
        self.chunk_size = 0
        self.tag = b'\x0C'

    def getBytes(self, data) -> []:
        self.chunk_size = self.getSize(data)
        return [struct.pack("<cIII", self.tag, self.chunk_id, self.chunk_version, self.chunk_size)] + data

    def getSize(self, data) -> int:
        result = 0
        for d in data:
            result = result + len(d)
        return result + 13
