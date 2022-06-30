import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type

class ReferenceToDataChunkReaderV0:
    def parse(self, f):
        name: max_type.parseType(f)
        return kf2_type.RefferenceToDataV0(0, name)