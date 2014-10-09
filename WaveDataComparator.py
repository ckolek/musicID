__author__ = 'Mike_Deniz'

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

        trace = 0

        # comparing each segment of wave1 to all in wave2
        # slower than going through each simultaneously, but will likely
        # be needed for final version
        for x in wave1segments:
            for y in wave2segments:
                # if the transforms of two segments match, return a match
                if self.compareTransform(fft(x), fft(y), trace):
                    return True
                trace += 1

        # If no segments matched throughout entire files, return False
        return False

    # Compares two discrete fourier transforms
    def compareTransform(self, dft1, dft2, x):

        # new comparison checks to see that all constituent frequencies
        # gotten from ffts of segments are no more than 1% different
        l1 = list(dft1)
        #l1.sort()
        #l1.reverse()
        l2 = list(dft2)
        #l2.sort()
        #l2.reverse()
    
        #convert lists to their sorted power spectral densities
        #where only the top 20% most powerful frequencies are present
        l1 = sorted(map(lambda x: abs(x)**2, l1), reverse=True)[0:int(len(l1)/5)]
        l2 = sorted(map(lambda x: abs(x)**2, l2), reverse=True)[0:int(len(l2)/5)]


        # double check to make sure lists are of equal size
        if len(l1) != len(l2):
            print "ERROR: problem in computing similarities"
            return False

        val = True
        # iterate through l1 and l2, check to see constituent frequencies are all very close
        for i in range(len(l1)):
            val = val and (.9 < (l1[i]/l2[i]) < 1.1)

        return val

