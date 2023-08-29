import max_payne_sdk.max_type_reader as mr

MAX_TYPE_STRING = b'\x0D'

MAX_TYPE_HANDLERS = {
    b'\x00': lambda f: mr.parseInt(f, 4, False),  # long
    b'\x01': lambda f: mr.parseInt(f, 4, True),  # unsigned long
    b'\x02': lambda f: mr.parseInt(f, 4, False),  # int
    b'\x03': lambda f: mr.parseInt(f, 4, True),  # unsigned int
    b'\x04': lambda f: mr.parseInt(f, 2, False),  # short
    b'\x05': lambda f: mr.parseInt(f, 2, True),  # unsigned short
    b'\x06': lambda f: mr.parseInt(f, 1, False),  # char
    b'\x07': lambda f: mr.parseInt(f, 1, False),  # signed char
    b'\x08': lambda f: mr.parseInt(f, 1, True),  # unsigned char
    b'\x09': lambda f: mr.parseFloat(f, 4),  # float
    b'\x0A': lambda f: mr.parseFloat(f, 8),  # double
    b'\x0D': lambda f, n: mr.parseString(f, n),  # string
    b'\x0E': lambda f: mr.parseInt(f, 1, True),  # bool
    b'\x0F': lambda f: mr.parseInt(f, 3, True),  # unsigned int
    b'\x10': lambda f: mr.parseInt(f, 2, True),  # unsigned int
    b'\x11': lambda f: mr.parseInt(f, 1, True),  # unsigned int
    b'\x12': lambda f: mr.parseInt(f, 3, False),  # int
    b'\x13': lambda f: mr.parseInt(f, 2, False),  # int
    b'\x14': lambda f: mr.parseInt(f, 1, False),  # int
    b'\x15': lambda f: mr.parseVector(f, 8),  # vector2d
    b'\x16': lambda f: mr.parseVector(f, 12),  # vector3d
    b'\x17': lambda f: mr.parseVector(f, 16),  # vector4d
    b'\x18': lambda f: mr.parseMatrix(f, 16),  # matrix2x2
    b'\x19': lambda f: mr.parseMatrix(f, 36),  # matrix3x3
    b'\x1A': lambda f: mr.parseMatrix(f, 48),  # matrix4x3
    b'\x1B': lambda f: mr.parseMatrix(f, 64),  # matrix4x4
    b'\x26': lambda f: mr.parseFloat(f, 2)  # float16
}


def parseType(f):
    typeID = f.read(1)
    if typeID == MAX_TYPE_STRING:
        return MAX_TYPE_HANDLERS[MAX_TYPE_STRING](f, MAX_TYPE_HANDLERS[f.read(1)](f))
    if typeID in MAX_TYPE_HANDLERS:
        return MAX_TYPE_HANDLERS[typeID](f)
    raise Exception("Undefined Type Tag", typeID.hex())


def parseFloat(f) -> float:
    return mr.parseFloat(f, 4)


def parseInt(f, bytes_to_read, is_unsigned) -> int:
    return mr.parseInt(f, bytes_to_read, is_unsigned)
