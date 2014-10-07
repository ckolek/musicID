import sys, os
from WaveDataComparator import WaveDataComparator
from wave.waveDataReader import WaveDataReader

__author__ = 'ckolek'


class MusicID:
    def __init__(self, file_names):
        self.file_names = file_names

    def run(self):
        if bad_file_check([self.file_names[0], self.file_names[1]]):
            return 1

        wave1 = read_wave_data(self.file_names[0])
        wave2 = read_wave_data(self.file_names[1])


        if WaveDataComparator.areMatching(wave1, wave2):
            print "MATCH " + self.file_names[0] + " " + self.file_names[1]
        else:
            print "NO MATCH"

        return 0


def read_wave_data(file_name):
    with WaveDataReader.open(file_name) as reader:
        return reader.read()

# checks to make sure files both exist and are .wav format
def bad_file_check(files):
    for file in files:
        # make sure file exists
        if not os.access(file, os.F_OK):
            print "ERROR: " + file + " does not exist"
            return True

        #make sure file is .wav
        if not file[len(file)-4:len(file)] == ".wav":
            print "ERROR: " + file + " is not a supported format"
            return True


if __name__ == '__main__':
    music_id = MusicID(sys.argv[1:])

    status = music_id.run()

    sys.exit(status)