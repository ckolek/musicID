__author__ = 'ckolek'

import struct


def unpack_from(data, offset, is_unsigned, signed_format, unsigned_format, is_little_endian):
    format = ('<' if is_little_endian else '>') + (unsigned_format if is_unsigned else signed_format)

    return struct.unpack_from(format, data, offset)[0]


def to_short(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'h', 'H', is_little_endian)


def to_int(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'i', 'I', is_little_endian)


def to_long(data, offset=0, is_unsigned=False, is_little_endian=True):
    return unpack_from(data, offset, is_unsigned, 'l', 'L', is_little_endian)