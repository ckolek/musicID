__author__ = 'ckolek'

import io
from waveData import WaveData
from util import utilities


class WaveDataReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self):
        chunk_id_buf = self.stream.read(4)

        if chunk_id_buf is None or len(chunk_id_buf) < 4:
            raise IOError('could not read chunk ID')

        chunk_id = chunk_id_buf.encode("ASCII")

        if chunk_id == 'RIFF':
            is_little_endian = True
        elif chunk_id == 'RIFX':
            is_little_endian = False
        else:
            raise IOError('invalid chunk ID: ' + chunk_id)

        chunk_size_buf = self.stream.read(4)

        if chunk_size_buf is None or len(chunk_size_buf) < 4:
            raise IOError('could not read chunk size')

        chunk_size = utilities.to_long(chunk_size_buf, is_unsigned=True, is_little_endian=is_little_endian)

        format_buf = self.stream.read(4)

        if format_buf is None or len(format_buf) < 4:
            raise IOError('could not read format_buf')

        format = format_buf.encode("ASCII")

        if not format == 'WAVE':
            raise IOError('invalid format: ' + format)

        length = 4

        chunks = set()

        while length < chunk_size:
            chunk = self.read_chunk(is_little_endian)

            length += 8 + chunk.length()

            chunks.add(chunk)

        return WaveData(chunk_id, is_little_endian, chunk_size, format, chunks)

    def read_chunk(self, is_little_endian):
        chunk_id_buf = self.stream.read(4)

        if chunk_id_buf is None or len(chunk_id_buf) < 4:
            raise IOError('could not read sub-chunk ID')

        chunk_id = chunk_id_buf.encode("ASCII")

        chunk_size_buf = self.stream.read(4)

        if chunk_size_buf is None or len(chunk_size_buf) < 4:
            raise IOError('could not read sub-chunk size')

        chunk_size = utilities.to_long(chunk_size_buf, is_unsigned=True, is_little_endian=is_little_endian)

        data = self.stream.read(chunk_size)

        if data is None or len(data) < chunk_size:
            raise IOError('did not read ' + chunk_size + ' bytes of sub-chunk')

        return WaveData.Chunk(chunk_id, data)

    def close(self):
        self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(file_name):
        return WaveDataReader(io.open(file_name, 'rb'))
    open = staticmethod(open)