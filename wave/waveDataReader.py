__author__ = 'ckolek'

import io
from waveData import WaveData
from util import utilities
from util.exceptions import InvalidFormatError

class WaveDataReader:
    """
    This class provides the mechanism to read a WaveData object from a stream of
     raw bytes.
    """

    def __init__(self, stream):
        """
        :param stream: an input stream
        """

        self.stream = stream

    def read(self):
        """
        :return: A WaveDataObject read from the stream
        :raises: InvalidFormatError - If the data is not in a valid WAVE format
        """

        chunk_id_buf = self.stream.read(4)

        if chunk_id_buf is None or len(chunk_id_buf) < 4:
            raise InvalidFormatError('could not read chunk ID')

        try:
            chunk_id = chunk_id_buf.encode("ASCII")
        except Exception as e:
            raise InvalidFormatError(e.message)

        if chunk_id == 'RIFF':
            is_little_endian = True
        elif chunk_id == 'RIFX':
            is_little_endian = False
        else:
            raise InvalidFormatError('invalid chunk ID: ' + chunk_id)

        chunk_size_buf = self.stream.read(4)

        if chunk_size_buf is None or len(chunk_size_buf) < 4:
            raise InvalidFormatError('could not read chunk size')

        chunk_size = utilities.to_long(chunk_size_buf,
                                       is_unsigned=True,
                                       is_little_endian=is_little_endian)

        format_buf = self.stream.read(4)

        if format_buf is None or len(format_buf) < 4:
            raise InvalidFormatError('could not read format_buf')

        format = format_buf.encode("ASCII")

        if not format == 'WAVE':
            raise InvalidFormatError('invalid format: ' + format)

        length = 4

        chunks = set()

        while length < chunk_size:
            chunk = self.read_chunk(is_little_endian)

            length += 8 + chunk.length()

            chunks.add(chunk)

        return WaveData(chunk_id, is_little_endian, chunk_size, format, chunks)

    def read_chunk(self, is_little_endian):
        """
        Reads a WAVE subchunk from the input stream.

        :param is_little_endian: True if data is stored in little-endian format,
         False otherwise
        :return: the new Chunk object
        :raises: InvalidFormatError - If the data is not in a valid WAVE format
        """

        chunk_id_buf = self.stream.read(4)

        if chunk_id_buf is None or len(chunk_id_buf) < 4:
            raise InvalidFormatError('could not read sub-chunk ID')

        try:
            chunk_id = chunk_id_buf.encode("ASCII")
        except:
            raise InvalidFormatError('non-ASCII chunk ID')
        
        chunk_size_buf = self.stream.read(4)

        if chunk_size_buf is None or len(chunk_size_buf) < 4:
            raise InvalidFormatError('could not read sub-chunk size')

        chunk_size = utilities.to_long(chunk_size_buf,
                                       is_unsigned=True,
                                       is_little_endian=is_little_endian)

        data = self.stream.read(chunk_size)

        if data is None or len(data) < chunk_size:
            raise InvalidFormatError('did not read ' + `chunk_size` +
                                     ' bytes of sub-chunk')

        return WaveData.Chunk(chunk_id, data)

    def close(self):
        """
        Closes the underlying stream.
        """
        self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(file_name):
        """
        Opens an input stream to read binary data from the file with the given
         name, and returns a WaveDataReader object which wraps the opened
         stream

        :param file_name: the name of the file to read from
        :return: the WaveDataReader object to read data from the file
        """
        return WaveDataReader(io.open(file_name, 'rb'))
    open = staticmethod(open)
