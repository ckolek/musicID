__author__ = 'ckolek'

import struct


def unpack_from(data, offset, is_unsigned, signed_format, unsigned_format,
                is_little_endian):
    """
    Extracts a simple value from an array of bytes.

    :param data: the array of bytes to extract the value from
    :param offset: the offset (in bytes) from the start of the array
    :param is_unsigned: True if the extracted value should be unsigned, False
     otherwise
    :param signed_format: The format string used in struct.unpack_from if the
     extracted value is signed
    :param unsigned_format: The format string used in struct.unpack_from if the
     extracted value is unsigned
    :param is_little_endian: True if the value is encoded in little-endian
     format, False otherwise
    :return: the extracted value
    """

    return struct.unpack_from(
        ('<' if is_little_endian else '>') +
        (unsigned_format if is_unsigned else signed_format),
        data,
        offset)[0]


def to_short(data, offset=0, is_unsigned=False, is_little_endian=True):
    """
    Extracts a short (16-bit) integer from an array of bytes.

    :param data: the array of bytes to extract the value from
    :param offset: the offset (in bytes) from the start of the array
    :param is_unsigned: True if the extracted value should be unsigned, False
     otherwise
    :param is_little_endian: True if the value is encoded in little-endian
     format, False otherwise
    :return: the extracted short value
    """

    return unpack_from(data, offset, is_unsigned, 'h', 'H', is_little_endian)


def to_int(data, offset=0, is_unsigned=False, is_little_endian=True):
    """
    Extracts an integer from an array of bytes.

    :param data: the array of bytes to extract the value from
    :param offset: the offset (in bytes) from the start of the array
    :param is_unsigned: True if the extracted value should be unsigned, False
     otherwise
    :param is_little_endian: True if the value is encoded in little-endian
     format, False otherwise
    :return: the extracted value
    """
    return unpack_from(data, offset, is_unsigned, 'i', 'I', is_little_endian)


def to_long(data, offset=0, is_unsigned=False, is_little_endian=True):
    """
    Extracts a long (32-bit) integer from an array of bytes.

    :param data: the array of bytes to extract the value from
    :param offset: the offset (in bytes) from the start of the array
    :param is_unsigned: True if the extracted value should be unsigned, False
     otherwise
    :param is_little_endian: True if the value is encoded in little-endian
     format, False otherwise
    :return: the extracted long value
    """
    return unpack_from(data, offset, is_unsigned, 'l', 'L', is_little_endian)


def to_integer(data, length, offset=0, is_unsigned=False,
               is_little_endian=True):
    """
    Extracts an integer value of a given length (in bytes) from the given array
     of bytes.

    :param data: the array of bytes to extract the value from
    :param length: the length (in bytes) of the value
    :param offset: the offset (in bytes) from the start of the array
    :param is_unsigned: True if the extracted value should be unsigned, False
     otherwise
    :param is_little_endian: True if the value is encoded in little-endian
     format, False otherwise
    :return: the extracted value
    """

    value = 0

    for i in xrange(length):
        b = ord(data[offset + i] if is_little_endian else data[
            offset + length - 1 - i])

        if is_unsigned:
            value += (0xFF & b) << (8 * i)
        else:
            value += b << (8 * i)

    return value