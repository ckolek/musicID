__author__ = 'ckolek'

from wave.waveDataFormat import WaveDataFormat


class WaveData:
    def __init__(self, chunk_id, is_little_endian, chunk_size, format, chunks):
        self.chunk_id = chunk_id
        self.is_little_endian = is_little_endian
        self.chunk_size = chunk_size
        self.format = format

        self.chunks = dict()

        for chunk in chunks:
            self.chunks[chunk.id] = chunk

        self._wave_data_format = None

    def chunk(self, chunk_id):
        return self.chunks[chunk_id]

    def get_wave_data_format(self):
        if self._wave_data_format is None:
            self._wave_data_format = WaveDataFormat.from_wave_data(self)

        return self._wave_data_format
    wave_data_format = property(get_wave_data_format)

    class Chunk:
        def __init__(self, id, data):
            self.id = id
            self.data = data

        def length(self):
            return len(self.data)