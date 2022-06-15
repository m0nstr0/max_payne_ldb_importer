import struct 

def parseInt(f, bytes_to_read, is_unsigned):
    bytes = f.read(bytes_to_read)
    if is_unsigned:
        return int.from_bytes(bytes, byteorder='little', signed=False)
    return int.from_bytes(bytes, byteorder='little', signed=True)

def parseFloat(f, bytes_to_read):
    bytes = f.read(bytes_to_read)
    if bytes_to_read == 4:
        return struct.unpack("<f", bytes)[0]
    if bytes_to_read == 8:
        return struct.unpack("<d", bytes)[0]
    return struct.unpack("<e", bytes)[0]

def parseVector(f, bytes_to_read):
    if bytes_to_read == 8:
        return [parseFloat(f, 4), parseFloat(f, 4)]
    if bytes_to_read == 12:
        return [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)]
    return [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)]

def parseMatrix(f, bytes_to_read):
    if bytes_to_read == 16:
        return [ 
            [parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4)]
        ]
    if bytes_to_read == 36:
        return [
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)]
        ]
    if bytes_to_read == 48:
        return [
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)]
        ]
    return [
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)],
            [parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4), parseFloat(f, 4)]
        ]

def parseString(f, letters_num):
    return f.read(letters_num).decode("utf-8")