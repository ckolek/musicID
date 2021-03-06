__author__ = 'Mike_Deniz'

from segmenter import Segmenter
import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.mlab as ml
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter
import os.path
import sys

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

# Ranges of frequencies for audio bands we want the relative power of
RANGES = [16, 32, 512, 2048, 8192, 16384]

# constant used to normalize FFT results
NORM_CONS = 5000.0

# constant used to determine how many nearby 'neighbors'
# to search in our LSH tables
LSH_SPAN = 25

# the sequence of numbers used in computing LSH values for fingerprints
WEIGHTS = [-2, 5, -1, 2, -4, -3, 3, 1, -5, 2]

# Limit the number of fingerprint kept in memory
LSH_LIMIT = 2250000
# Each fingerprint is 80 bytes long, with average length songs (~3mins) at
# 2.5s segments that'd fingerprints would be 5760 bytes per song. At a 200MB
# memory limit, we could concievably keep the fingerprints for 34,700 songs in
# memory, which would be 2,498,400 fingerprints (at 2.5 segment lengths).
# To be conservative and account for other things we might be keeping in memory,
# the LSH_LIMIT value has been set to 2.25 million.


writtenToDisk = []

class WaveDataComparator:
    def __init__(self, num_banks):
        self.fingerprints = list()
        self.lshs = list()
        self.num_fingerprints = 0

        for i in range(num_banks):
            self.fingerprints.append(dict())
            self.lshs.append(dict())

        self.debug = False

    def register_sound(self, file_name, wave, bank_index):
        if self.debug:
            print "registering sound: %s [bank: %d]" % (file_name, bank_index)

        # create fingerprint for the sound
        fingerprints = self.makeFingerprints(file_name, wave)

        if self.debug:
            print "\tcreated %d fingerprints" % len(fingerprints)

        # associate fingerprint with file name
        self.fingerprints[bank_index][file_name] = fingerprints
        
        lsh = self.lshs[bank_index]

        # add fingerprints to LSH tables
        for fingerprint in fingerprints:
            # only keep LSH_LIMIT fingerprints in memory
            if self.num_fingerprints < LSH_LIMIT:
                hash_value = fingerprint.hash_value
                
                if not lsh.has_key(hash_value):
                    lsh[hash_value] = [fingerprint]
                else:
                    lsh[hash_value].append(fingerprint)
            # write all others to disk
            else:
                self.writeToDisk(fingerprint)
            
            self.num_fingerprints += 1

    # Compare function: computes 2 LSH tables for given fingerprints
    # and compares the fingerprints
    def compare(self):
        lsh1, lsh2 = self.lshs[0:2]

        # instantiate a list for seeing which audio tracks have matched
        # with each other to avoid repeats
        matched = []

        # go through fingerprints in LSH1, compare them
        # to values of close hashes in LSH2
        keys1 = sorted(lsh1.keys())
        keys2 = sorted(lsh2.keys())

        # go through keys in lsh1, each time find the nearest
        # neighbor keys in lsh2, and compare values in lsh1 hashed to k
        # to things hashed to nearby values in lsh2
        for key1 in keys1:
            span = (key1-LSH_SPAN, key1+LSH_SPAN)

            l2 = []
            for key2 in keys2:
                if key2 < span[0]:
                    continue
                elif key2 > span[1]:
                    break
                else:
                    l2.extend(lsh2[key2])

            for fp1 in lsh1[key1]:
                for fp2 in l2:
                    pair = (fp1.file_name, fp2.file_name)

                    if pair not in matched and self.are_matching(fp1, fp2):
                        matched.append(pair)

                        self.print_match(fp1, fp2)

    # check if the fingerprints mark the start of a matching segment of audio
    #  of at least 5 seconds in length
    def are_matching(self, fp1, fp2):
        if not self.compare_fprints(fp1, fp2):
            return False

        sound1_fps = self.fingerprints[0][fp1.file_name]
        sound2_fps = self.fingerprints[1][fp2.file_name]

        matching_count = 1

        # loop through all remaining fingerprints in sounds being compared
        while True:
            _fp1_index = fp1.index + matching_count
            _fp2_index = fp2.index + matching_count

            # check if we have passed the last fingerprints
            if _fp1_index >= len(sound1_fps) or _fp2_index >= len(sound2_fps):
                return False

            _fp1 = sound1_fps[_fp1_index]
            _fp2 = sound2_fps[_fp2_index]

            _fp1_offset = _fp1.start_time - fp1.start_time
            _fp2_offset = _fp2.start_time - fp2.start_time

            if _fp1.index - fp1.index > 0:
                return True

            # check if the current fingerprints match
            if not self.compare_fprints(_fp1, _fp2):
                return False

            matching_count += 1

    # compares two fingerprints, returns true if a match is found
    def compare_fprints(self, fp1, fp2):
        # value, will turn false if anything is found to be inconsistent
        val = True

        # extract fingerprint values from fingerprint class
        fp1v = fp1.values
        fp2v = fp2.values

        # fingerprints may contain frequency band strengths that
        # are miniscule compared to all others. If this is the case
        # simply set them to 1 for the comparison
        a1 = sum(fp1v[0:5])/5
        a2 = sum(fp2v[0:5])/5

        # assume that any band strengths that are less than 1/10th
        # are too small to be considered for comparison
        for i in range(5):
            if fp1v[i] <= a1/10:
                fp1v[i] = 1
            if fp2v[i] <= a2/10:
                fp2v[i] = 1


        # check to see our amplitudes of frequency bands
        # are of similar value
        for i in range(5):
            bv1 = fp1v[i]
            bv2 = fp2v[i]

            # if band power values are zero, simply change them to number
            # very close to 0 for division purposes
            if bv1 == 0:
                bv1 = 0.000000001
            if bv2 == 0:
                bv2 = 0.000000001

            val = val and (.9 <= bv1/bv2 <= 1.1)

        # next, see if frequencies in the fingerprints are similar
        for i in range(6,10):

            fv1 = fp1v[i]
            fv2 = fp2v[i]

            # if frequencies are zero, simply change them to number very close
            # to 0 for division purposes
            if bv1 == 0:
                bv1 = 0.000000001
            if bv2 == 0:
                bv2 = 0.000000001

            val = val and (.9 <= fv1/fv2 <= 1.1)

        return val

    # this function returns a list of fingerprints for a given file
    def makeFingerprints(self, file_name, wave):
        # Get a list of segments to be fingerprinted
        segmenter = Segmenter()
        segmenter.debug = self.debug

        segList = segmenter.segment_data(wave)

        # array where fingerprints will be stored
        fprints = []

        # Go through this list of segments, converting each segment
        # in place into its corresponding fingerprint
        # conversions will be to a tuple of the form:
        # (fingerprint, time offset of that fingerprint, file name)
        for i, segment in enumerate(segList):
            samples, start_time = segment

            segment_len = len(samples)

            frequencies = list(fftfreq(segment_len, 1.0 /
                wave.wave_data_format.sample_rate))

            bands = []
            t = 0
            for x in range(len(frequencies)):
                if t == len(RANGES):
                    break
                if frequencies[x] > RANGES[t]:
                    bands.append(x)
                    t += 1

            values = self.fingerprint(samples, frequencies, bands)

            hash_value = self.hashFunct(values)

            fprints.append(Fingerprint(file_name,
                                       start_time,
                                       values,
                                       hash_value,
                                       frequencies,
                                       bands,
                                       i))

        return fprints

    # compute a fingerprint for a given range of samples
    def fingerprint(self, samples, frequencies, bands):
        # take an fft over our samples and convert the complex values
        # to their magnitudes (only take positive frequencies, then normalize
        samples = list(fft(samples))
        samples = map(abs, samples[0:len(samples)/2])
        self.normalize(samples)

        # our final fprint is a list corresponding to 'powers' of
        # certain bands of frequencies
        fprint = []
        for x in range(len(bands)-1):
            fprint.append(sum(samples[bands[x]:bands[x+1]]))

        # next, sort the samples and get the strongest frequencies
        # present in each group of samples
        top5 = []
        for x in sorted(samples, reverse=True)[0:5]:
            top5.append(frequencies[samples.index(x)])

        top5 = sorted(top5)

        return fprint+top5

    # a hash function for our LSH tables, takes a fingerprint
    # and returns a hashvalue for that fingerprint
    def hashFunct(self, fprint_values):
        # the hash function will be a sequence of weights times
        # the band strengths plus the average of the strongest frequencies
        val = 0
        lw = len(WEIGHTS)
        for x in range(lw):
            val += WEIGHTS[x]*(fprint_values[x]/100.0)

        return int(val)

    # Write the given fingerprint to disk, naming the file after the hashkey
    # Append the hashkey to a list of things we've written to disk
    def writeToDisk(self, fingerprint):
        # Get our current directory
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # Set our destination directory /tmp/
        dest_dir = os.path.join(cur_dir, 'tmp')
        # Try to make the tmp dir
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass  # Already exists
        # Create our target path
        path = os.path.join(dest_dir, str(fingerprint.hash_value)+'.txt')
        # Write fingerprint to disk
        with open(path, 'a') as stream:  # Open file in append mode
            stream.write(str(fingerprint))
            stream.write('\n')

        # Add hashkey to LOthings We've Written
        writtenToDisk.append(fingerprint.hash_value)
        stream.close()

    # Given a hashkey, try to find the corresponding fingerprint txt file
    def readFromDisk(self, key):
        try:
            f = open('tmp/'+str(key)+".txt", 'r') # Open file in read mode
            return f.read()
        except (OSError, IOError) as e:
            return  # File not found

    # normalizes an array to a defined max value, maintaining
    # ratios between numbers in the array
    def normalize(self, a):
        # get the ratio between the largest member in the array and
        # our normalizing constant
        ratio = float(max(a))/NORM_CONS

        # check to make sure ratio doesn't wind up 0 
        # (could happen during segments of silence)
        if ratio == 0:
            ratio = 1.0

        # divide all members in the array by the ratio
        for i in range(len(a)):
            try:
                a[i] = a[i]/ratio
            except RuntimeWarning:
                print a[i]


    # print the string resulting in matching two fingerprints
    def print_match(self, fp1, fp2):
        s = "MATCH %s %s %s %s"

        # extract short names of our files
        fn1 = fp1.file_name.split('/')
        fn1 = fn1[len(fn1)-1]

        fn2 = fp2.file_name.split('/')
        fn2 = fn2[len(fn2)-1]

        # get times rounded to nearest tenth
        t1 = str(round(fp1.start_time, 1))
        t2 = str(round(fp2.start_time, 1))

        print (s % (fn1, fn2, t1, t2))

# A class that holds information about the fingerprint of a segment of
#  WAVE audio
class Fingerprint:
    def __init__(self, file_name, start_time, values, hash_value,
            frequencies, bands, index):
        """
        :param file_name: the name of the file the audio is from
        :param start_time: the offset in time of the segment within the
          complete audio
        :param values: the fingerprint values
        :param hash_value: the hashed value of the fingerprint values
          (for LSH)
        :param frequencies: 
        :param bands: 
        :param index: the index of the segment within the complete
          collection of segments for the audio
        """

        self.file_name = file_name
        self.start_time = start_time
        self.values = values
        self.hash_value = hash_value
        self.frequencies = frequencies
        self.bands = bands
        self.index = index

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}|{}|{}|{}|{}".format(self.file_name,
                                             self.start_time,
                                             self.values,
                                             self.hash_value,
                                             self.index)

    def parse(string):
        parts = string.split('|')

        file_name = parts[0]
        start_time = float(parts[1])
        values = map(parts[2][1:-2].split(','), lambda s: float(s.strip()))
        hash_value = int(parts[3])
        index = int(parts[4])

        return Fingerprint(file_name, start_time, values, hash_value, index)
