"""Shared binary I/O checks; no Maya dependency."""


class FormatError(ValueError):
    """The input does not contain the expected serialized record."""


def read_exact(stream, size):
    if not isinstance(size, int) or size < 0:
        raise FormatError("Invalid byte count: %r" % (size,))
    offset = stream.tell()
    data = stream.read(size)
    if len(data) != size:
        raise FormatError("Truncated input at 0x%x: expected %d bytes, got %d"
                          % (offset, size, len(data)))
    return data


def read_count(stream):
    # Import locally because tagged primitives use read_exact too.
    from max_payne_sdk.max_type import parseType
    count = parseType(stream)
    if not isinstance(count, int) or count < 0:
        raise FormatError("Invalid element count: %r" % (count,))
    return count
