__author__ = 'ckolek'

import struct


def unpack_from(data, offset, is_unsigned, signed_format, unsigned_format, is_little_endian):
    return struct.unpack_from(
        ('<' if is_little_endian else '>') + (unsigned_format if is_unsigned else signed_format),
        data,
        offset)[0]


def to_short(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'h', 'H', is_little_endian)


def to_int(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'i', 'I', is_little_endian)


def to_long(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'l', 'L', is_little_endian)


def to_integer(data, length, offset=0, is_unsigned=False, is_little_endian=True):
    value = 0

    for i in xrange(length):
        b = ord(data[offset + i] if is_little_endian else data[offset + length - 1 - i])

        if is_unsigned:
            value += (0xFF & b) << (8 * i)
        else:
            value += b << (8 * i)

    return value