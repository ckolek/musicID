import sys
from wave.waveDataReader import WaveDataReader
from wave.waveDataFormat import WaveDataFormat

__author__ = 'ckolek'

class MusicID:
    def __init__(self, file_names):
        self.file_names = file_names

    def run(self):
        waves = []

        for file_name in self.file_names:
            print 'File: ', file_name

            with WaveDataReader.open(file_name) as reader:
                wave = reader.read()

                display_wave(wave)

                waves.append(wave)

        return 0


def display_wave(wave):
    print 'Chunk ID: ', wave.chunk_id
    print 'Chunk Size: ', wave.chunk_size
    print 'Format: ', wave.format
    print 'Chunks: ', wave.chunks.keys()

    format = WaveDataFormat.from_wave_data(wave)

    print 'Audio Format: ', format.audio_format
    print 'Num Channels: ', format.num_channels
    print 'Sample Rate: ', format.sample_rate
    print 'Byte Rate', format.byte_rate
    print 'Block Align: ', format.block_align
    print 'Bits Per Sample: ', format.bits_per_sample
    print 'Bytes Per Sample: ', format.bytes_per_sample

if __name__ == '__main__':
    id = MusicID(sys.argv[1:])

    status = id.run()

    sys.exit(status)