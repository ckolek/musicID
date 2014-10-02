__author__ = 'ckolek'


class WaveData:
    def __init__(self, chunk_id, is_little_endian, chunk_size, format, chunks):
        self.chunk_id = chunk_id
        self.is_little_endian = is_little_endian
        self.chunk_size = chunk_size
        self.format = format

        self.chunks = dict()

        for chunk in chunks:
            self.chunks[chunk.id] = chunk

    def chunk(self, chunk_id):
        return self.chunks[chunk_id]

    class Chunk:
        def __init__(self, id, data):
            self.id = id
            self.data = data

        def length(self):
            return len(self.data)

        def extract_channels(self, format):
            channel_size = self.length() / format.num_channels
            num_samples = channel_size / format.bytes_per_sample

            channel_data = []

            for i in xrange(format.num_channels):
                channel_data.append([])

            for i in xrange(num_samples):
                for j in xrange(format.num_channels):
                    for k in xrange(format.bytes_per_sample):
                        channel_data[j][(i * format.bytes_per_sample) + k] =\
                            self.data[(i * format.block_align) + (j * format.bytes_per_sample) + k];

            return channel_data