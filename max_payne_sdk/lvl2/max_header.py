from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packInt, packString


class MaxHeader:
    def __init__(self) -> None:
        self.version_string = "MAXED1.1"
        self.version = 3
        self.build_string = "2.0 build 103"

    def getBytes(self) -> []:
        data = [packString(self.version_string), packInt(self.version), packString(self.build_string)]
        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data)

