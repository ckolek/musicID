__author__ = 'Mike_Deniz'

import Segmenter
import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.mlab as ml
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter

IDX_FREQ_I = 0
IDX_TIME_J = 1

'''
CREDIT TO:
Dejavu library
   github.com/worldveil/dejavu
'''

# Sampling rate, related to the Nyquist conditions, which affects
# the range frequencies we can detect.
DEFAULT_FS = 44100

# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

# Degree to which a fingerprint can be paired with its neighbours;
# higher will cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

# Number of cells around an amplitude peak in the spectrogram in order
# to consider it a spectral peak. Higher values mean less fingerprints and
# faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

# If True, will sort peaks temporally for fingerprinting;
# not sorting will cut down number of fingerprints, but potentially
# affect performance.
PEAK_SORT = True

# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. The more you throw away, the less storage, but
# potentially higher collisions and misclassification's when identifying songs.
FINGERPRINT_REDUCTION = 20

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
        for x in wave1list:
            #x = self.makeFftList(x, float(waveDataFormat1.sample_rate))
            x = self.fingerprint(x, DEFAULT_FS, DEFAULT_WINDOW_SIZE,
                                 DEFAULT_OVERLAP_RATIO, DEFAULT_FAN_VALUE,
                                 DEFAULT_AMP_MIN)
            #print x
            for y in wave2list:
                #y = self.makeFftList(y, float(waveDataFormat2.sample_rate))
                y = self.fingerprint(y, DEFAULT_FS, DEFAULT_WINDOW_SIZE,
                                     DEFAULT_OVERLAP_RATIO, DEFAULT_FAN_VALUE,
                                     DEFAULT_AMP_MIN)
                # if the transforms of two segments match, return a match
                if self.compareTransform(x, y):
                    return True

        # If no segments matched throughout entire files, return False
        return False

    # Compares two discrete fourier transforms
    def compareTransform(self, dft1, dft2):

        # new comparison checks to see that all constituent frequencies
        # gotten from ffts of segments are no more than 1% different
        l1 = list(dft1)
        l2 = list(dft2)

        #convert lists to their sorted power spectral densities
        #where only the top 20% most powerful frequencies are present
        spec_dens = lambda x: (abs(x[0])**2, x[1])
        l1 = sorted(map(spec_dens, l1), reverse=True)[0:7]
        l2 = sorted(map(spec_dens, l2), reverse=True)[0:7]

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

    def fingerprint(self, channel_samples, Fs=DEFAULT_FS,
                    wsize=DEFAULT_WINDOW_SIZE,
                    wratio=DEFAULT_OVERLAP_RATIO,
                    fan_value=DEFAULT_FAN_VALUE,
                    amp_min=DEFAULT_AMP_MIN):
        """
        FFT the channel, log transform output, find local maxima, then return
        locally sensitive hashes.
        """
        # FFT the signal and extract frequency components
        spectrogram = ml.specgram(
            channel_samples,
            NFFT=wsize,
            Fs=Fs,
            window=ml.window_hanning,
            noverlap=int(wsize * wratio))[0]

        # apply log transform since specgram() returns linear array
        spectrogram = 10 * np.log10(spectrogram)
        #print "POST LOG SPECTROGRAM:\n" + str(spectrogram)
        spectrogram[spectrogram == -np.inf] = 0  # replace infs with zeros
        #print "POST INF REPLACEMENT SPECTROGRAM:\n" + str(spectrogram)

        # find local maxima
        print spectrogram
        local_maxima  = self.get_peaks(spectrogram, plot=False, amp_min=amp_min)

        #print "LOCAL MAXIMA\n" + str(local_maxima)

        # return hashes
        return self.generate_hashes(local_maxima, fan_value=fan_value)

    def get_peaks(self, spectrogram, plot=False, amp_min=DEFAULT_AMP_MIN):

        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)
        #print "NEIGH:\n" + str(neighborhood)

        #print "Spectrogram:\n " + str(spectrogram) + "\n Neighborhood:\n" + str(neighborhood)

        # find local maxima using our fliter shape
        local_max = maximum_filter(spectrogram, footprint=neighborhood) == spectrogram
        background = (spectrogram == 0)
        eroded_background = binary_erosion(background, structure=neighborhood,
                                           border_value=1)

        #print "LOCAL MAX:\n" + str(local_max)
        #print 'BG:\n' + str(background)
        #print "ERODED BG:\n" + str(eroded_background)

        # Boolean mask of spectrogram with True at peaks
        detected_peaks = local_max - eroded_background

        # extract peaks
        amps = spectrogram[detected_peaks]
        #print "PRE-FLATTEN AMPS:\n" + str(amps)
        j, i = np.where(detected_peaks)

        # filter peaks
        amps = amps.flatten()
        #print "POST-FLATTEN AMPS:\n" + str(amps)
        peaks = zip(i, j, amps)
        #print "PEAKS:\n" + str(peaks)

        #FIXME: PEAK FILTERING returns empty list because all of the amplitudes
        #FIXME: are negative numbers for some reason.
        peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

        #print "PEAKS FILTERED:\n" + str(peaks_filtered)

        # get indices for frequency and time
        frequency_idx = [x[1] for x in peaks_filtered]
        time_idx = [x[0] for x in peaks_filtered]

        if plot:
            # scatter of the peaks
            fig, ax = plt.subplots()
            ax.imshow(spectrogram)
            ax.scatter(time_idx, frequency_idx)
            ax.set_xlabel('Time')
            ax.set_ylabel('Frequency')
            ax.set_title("Spectrogram")
            plt.gca().invert_yaxis()
            plt.show()

        return zip(frequency_idx, time_idx)

    def generate_hashes(self, peaks, fan_value=DEFAULT_FAN_VALUE):
        """
        Hash list structure:
           sha1_hash[0:20]    time_offset
        [(e05b341a9b77a51fd26, 32), ... ]
        """
        fingerprinted = set()  # to avoid rehashing same pairs

        if PEAK_SORT:

            peaks.sort(key=itemgetter(1))

        for i in range(len(peaks)):
            for j in range(1, fan_value):
                if (i + j) < len(peaks) and not (i, i + j) in fingerprinted:
                    freq1 = peaks[i][IDX_FREQ_I]
                    freq2 = peaks[i + j][IDX_FREQ_I]

                    t1 = peaks[i][IDX_TIME_J]
                    t2 = peaks[i + j][IDX_TIME_J]

                    t_delta = t2 - t1

                    if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
                        h = hashlib.sha1(
                            "%s|%s|%s" % (str(freq1), str(freq2), str(t_delta)))
                        yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)

                    # ensure we don't repeat hashing
                    fingerprinted.add((i, i + j))






















