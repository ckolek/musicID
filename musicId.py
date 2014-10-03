import sys
from wave.waveDataReader import WaveDataReader

__author__ = 'ckolek'


class MusicID:
    def __init__(self, file_names):
        self.file_names = file_names

    def run(self):
        wave1 = read_wave_data(self.file_names[0])
        wave2 = read_wave_data(self.file_names[1])

        return 0


def read_wave_data(file_name):
    with WaveDataReader.open(file_name) as reader:
        return reader.read()


if __name__ == '__main__':
    music_id = MusicID(sys.argv[1:])

    status = music_id.run()

    sys.exit(status)