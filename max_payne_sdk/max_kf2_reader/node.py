import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type

class NodeChunkReaderV1:
    def parse(self, f):
        name = max_type.parseType(f)
        parent_name = max_type.parseType(f)
        object_to_parent_tranform = max_type.parseType(f)
        has_parent = max_type.parseType(f)
        user_defined_string = max_type.parseType(f)
        return kf2_type.NodeV1(1, name, parent_name, object_to_parent_tranform, has_parent, user_defined_string)