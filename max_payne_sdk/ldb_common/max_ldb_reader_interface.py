from max_payne_sdk.ldb_common.max_ldb_interface import MaxLDBInterface


class MaxLDBReaderInterface:
    def __init__(self, file_path: str):
        self.file_path = file_path
        pass

    def parse(self) -> MaxLDBInterface:
        pass
