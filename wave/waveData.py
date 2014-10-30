__author__ = 'ckolek'

from wave.waveDataFormat import WaveDataFormat

class WaveData:
    """
    Represents all of the data found in a WAVE file including header information
     such as:
        - Chunk ID
        - Chunk Size
        - Format

     as well as all of the chunks of the data.
    """

    def __init__(self, chunk_id, is_little_endian, chunk_size, format, chunks):
        """
        :param chunk_id: the Chunk ID (4-byte string)
        :param is_little_endian: True if chunk_id == "RIFF", False if
            chunk_id == "RIFX"
        :param chunk_size: the Chunk Size (in bytes) of the WAVE data
        :param format: the WAVE format (4-byte string)
        :param chunks: a collection of the Chunks of the WAVE data
        """

        self.chunk_id = chunk_id
        self.is_little_endian = is_little_endian
        self.chunk_size = chunk_size
        self.format = format

        self.chunks = dict()

        for chunk in chunks:
            self.chunks[chunk.id] = chunk

        self._wave_data_format = None

    def chunk(self, chunk_id):
        """
        :param chunk_id: The Chunk ID of the subchunk to retrieve
        :return: the subchunk of the WAVE data with the given Chunk ID
        """

        return self.chunks[chunk_id]

    def get_wave_data_format(self):
        """
        :return: the WaveDataFormat object for this WaveData object
        """
        if self._wave_data_format is None:
            self._wave_data_format = WaveDataFormat.from_wave_data(self)

        return self._wave_data_format
    wave_data_format = property(get_wave_data_format)

    class Chunk:
        """
        Represents a subchunk of WAVE data including the Chunk ID and raw data
        """

        def __init__(self, id, data):
            """
            :param id: the Chunk ID of the subchunk
            :param data: the raw data of the subchunk
            """

            self.id = id
            self.data = data

        def length(self):
            """
            :return: the length (in bytes) of the raw data of the subchunk
            """

            return len(self.data)