from max_payne_sdk.max_ldb import MaxLDBReader
from max_payne_sdk.max_ldb2 import MaxLDBReader2
from max_payne_sdk.ldb_common.max_ldb_reader_interface import MaxLDBReaderInterface


class MaxLBDReaderFactory:
    @staticmethod
    def createReader(file_path: str) -> MaxLDBReaderInterface:
        is_ldb2: bool = False
        with open(file_path, "rb") as f:
            ldb2_header = int.from_bytes(f.read(4), byteorder='little', signed=False)
            if ldb2_header == 843203660:
                is_ldb2 = True
        if is_ldb2:
            return MaxLDBReader2(file_path)
        else:
            return MaxLDBReader(file_path)