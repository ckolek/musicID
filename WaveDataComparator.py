__author__ = 'Deniz'

import Segmenter
from numpy.fft import fft


class WaveDataComparator:
    def __init__(self, wave1, wave2):
        self.wave1 = wave1
        self.wave2 = wave2

    def areMatching(self):
        waveDataFormat1 = self.wave1.wave_data_format
        waveDataFormat2 = self.wave2.wave_data_format

        chunk1 = self.wave1.chunk("data")
        chunk2 = self.wave2.chunk("data")

        # Check if files are same length in time
        if waveDataFormat1.get_time(chunk1) != waveDataFormat2.get_time(chunk2):
            return False

        wave1segments = Segmenter.segment_data(self.wave1)
        wave2segments = Segmenter.segment_data(self.wave2)

        # comparing each segment of wave1 to all in wave2
        # slower than going through each simultaneously, but will likely
        # be needed for final version
        for x in wave1segments:
            for y in wave2segments:
                # if the transforms of two segments match, return a match
                if WaveDataComparator.compareTransform(fft(x), fft(y)):
                    return True

        # If no segments matched throughout entire files, return False
        return False

    # Compares two discrete fourier transforms
    def compareTransform(self, dft1, dft2):

        # for now simply see if they are an exact match, will likely
        # need to be edited
        return list(dft1) == list(dft2)


