__author__ = 'Mike_Deniz'

import Segmenter
from numpy.fft import fft, fftfreq
import matplotlib.mlab as ml


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
        t1 = waveDataFormat1.get_time(chunk1)
        t2 = waveDataFormat2.get_time(chunk2)
        if t1 != t2:
            return False

        wave1list = Segmenter.segment_data(self.wave1)
        wave2list = Segmenter.segment_data(self.wave2)

        # MAY BE DELETED
        # convert list of wave file segments to lists of spectrograms
        # of corresponding segments
        #to_specgram =
        # lambda x: ml.specgram(x, Fs=waveDataFormat1.sample_rate)
        #wave1list = map(to_specgram, wave1list)
        #wave2list = map(to_specgram, wave2list)


        # comparing each segment of wave1 to all in wave2
        # slower than going through each simultaneously, but will likely
        # be needed for final version
        trace = 0
        for x in wave1list:
            x = self.makeFftList(x, float(waveDataFormat1.sample_rate))
            for y in wave2list:
                y = self.makeFftList(y, float(waveDataFormat2.sample_rate))
                # if the transforms of two segments match, return a match
                if self.compareTransform(x, y, trace):
                    return True
                trace += 1


        # If no segments matched throughout entire files, return False
        return False

    # Compares two discrete fourier transforms
    def compareTransform(self, dft1, dft2, trace):

        # new comparison checks to see that all constituent frequencies
        # gotten from ffts of segments are no more than 1% different
        l1 = list(dft1)
        l2 = list(dft2)
    
        #convert lists to their sorted power spectral densities
        #where only the top 20% most powerful frequencies are present
        spec_dens = lambda x: (abs(x[0])**2, x[1])
        l1 = sorted(map(spec_dens, l1), reverse=True)[0:7]
        l2 = sorted(map(spec_dens, l2), reverse=True)[0:7]

        if trace == 0:
            print l1
            print l2

        val = True
        # iterate through l1 and l2, check to see strengths of frequencies
        # are very close and frequencies themselves are all very close
        for i in range(len(l1)):
            val = val and (.9 < (l1[i][0]/l2[i][0]) < 1.1)
            val = val and abs(l1[i][1]-l2[i][1]) < 5

        return val

    # computes an 'fft list' for a segment of samples. This is a list of
    # pairs (strength of frequency, frequency)
    # l is a list of samples, n is the sampling rate
    def makeFftList(self, l, n):

        l = list(fft(l))

        return zip(l, fftfreq(len(l), 1/n))[0:len(l)/2]























