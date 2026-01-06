import struct


def packUInt(value):
    return struct.pack("<cI", b'\x03', value)


def packInt(value):
    return struct.pack("<ci", b'\x02', value)


def packString(value):
    return struct.pack("<cci" + str(len(value)) + "s", b'\x0D', b'\x02', len(value), value.encode("latin1"))


def packDouble(value):
    return struct.pack("<cd", b'\x0A', value)


def packBool(value):
    return struct.pack("<c?", b'\x0E', value)


def packULong(value):
    return struct.pack("<cI", b'\x01', value)


def packFloat(value):
    return struct.pack("<cf", b'\x09', value)


def packVector3(value):
    return struct.pack("<cfff", b'\x16', value[0], value[1], value[2])


def packUChar(value):
    return struct.pack("<cB", b'\x08', value)
