__author__ = 'Deniz'

import Segmenter
from numpy import fft


class WaveDataComparator:
    def areMatching(wave1, wave2):
        waveDataFormat1 = wave1.wave_data_format
        waveDataFormat2 = wave2.wave_data_format

        chunk1 = wave1.chunk("data")
        chunk2 = wave2.chunk("data")

        # Check if files are same length in time
        if waveDataFormat1.get_time(chunk1) != waveDataFormat2.get_time(chunk2):
            return False

        wave1segments = Segmenter.segment_data(wave1)
        wave2segments = Segmenter.segment_data(wave2)

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
        return dft1 == dft2

    areMatching = staticmethod(areMatching)