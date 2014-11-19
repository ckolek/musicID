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

# samples in a given segment
SAMPLES_PER_SEGMENT = Segmenter.SAMPLES_PER_SEGMENT

# Ranges of frequencies for audio bands we want the relative power of
RANGES = [16, 32, 512, 2048, 8192, 16384]

# Frequencies generated by the FFT on an array of size 8192
FREQS = list(fftfreq(8192, 1.0/DEFAULT_FS))[1:SAMPLES_PER_SEGMENT/2]

# the array indicies for the ranges of the frequencies above
BANDS = []
t = 0
for x in range(len(FREQS)):
    if t == len(RANGES):
        break
    if FREQS[x] > RANGES[t]:
        BANDS.append(x)
        t += 1

# constant used to normalize FFT results
NORM_CONS = 5000.0

# constant used to determine how many nearby 'neighbors'
# to search in our LSH tables
LSH_SPAN = 15

# the sequence of numbers used in computing LSH values for fingerprints
WEIGHTS = [-2, 5, -1, 2, -4, -3, 3, 1, -5, 2]

# Limit the number of fingerprint kept in memory
LSH_LIMIT = 2250000
# Each fingerprint is 80 bytes long, with average length songs (~3mins) at
# 2.5s segments fingerprints would be 5760 bytes per song. With a 200MB
# memory limit, we could conceivably keep the fingerprints for 34,700 songs in
# memory, which would be 2,498,400 fingerprints (at 2.5 segment lengths).
# To be conservative and account for other things we might be keeping in memory,
# the LSH_LIMIT value has been set to 2.25 million.

# Keeps track of what we've written to disk
writtenToDisk = []

class WaveDataComparator:
    def __init__(self, set1, set2):
        self.set1 = set1
        self.set2 = set2


    # Compare function: computes 2 LSH tables for given fingerprints
    # and compares the fingerprints
    def compare(self):

        # two LSH tables to be used for comparisons
        lsh1 = {}
        lsh2 = {}

        lshCnt = 0
        limitHitp = False

        # get fingerprints for files in set 1, and add them
        # to lsh1
        for x in self.set1:
            x = self.makeFingerprints(x)
            for f in x:
                hx = self.hashFunct(f)

                # Check if the fingerprint limit has been reached
                if lshCnt > LSH_LIMIT:
                    if hx not in lsh2:
                        lsh2[hx] = "wroteToDisk"
                        # Write the remaining fingerprints to disk
                        self.writeToDisk(hx, f)
                    # otherwise, if that key already exists in the
                    # LSH table
                    else:
                        f = lsh2[hx] + f
                        lsh2[hx] = "wroteToDisk"
                        # Write the fingerprints to disk
                        self.writeToDisk(hx, f, isList=True)

                if limitHitp is False:
                    if hx in lsh1 and (limitHitp is False):
                        lsh1[hx].append(f)
                    else:
                        lsh1[hx] = [f]
                    lshCnt += 1  # Increment shared lsh counter

        # repeat above process for set 2 and lsh2
        for x in self.set2:
            x = self.makeFingerprints(x)
            for f in x:
                hx = self.hashFunct(f)

                # Check if the fingerprint limit has been reached
                if lshCnt > LSH_LIMIT:
                    limitHitp = True
                    # if that hash value is not yet in the LSH table...
                    if hx not in lsh2:
                        lsh2[hx] = "wroteToDisk"
                        # Write the remaining fingerprints to disk
                        self.writeToDisk(hx, f)
                    # otherwise, if that key already exists in the
                    # LSH table
                    else:
                        f = lsh2[hx] + f
                        lsh2[hx] = "wroteToDisk"
                        # Write the fingerprints to disk
                        self.writeToDisk(hx, f, isList=True)


                if limitHitp is False:
                    if hx in lsh2 and (limitHitp is False):
                        lsh2[hx].append(f)
                    else:
                        lsh2[hx] = [f]
                    lshCnt += 1  # Increment shared lsh counter

        # instantiate a list for seeing which audio tracks have matched
        # with each other to avoid repeats
        matched = []

        # go through fingerprints in LSH1, compare them
        # to values of close hashes in LSH2
        k1 = sorted(lsh1.keys())
        k2 = sorted(lsh2.keys())
        lk2 = len(k2)

        # go through keys in lsh1, each time find the nearest
        # neighbor keys in lsh2, and compare values in lsh1 hashed to k
        # to things hashed to nearby values in lsh2
        for k in k1:
            span = (k-LSH_SPAN, k+LSH_SPAN)
            l2 = []
            for v in k2:
                if span[1] >= v >= span[0]:
                    # Check if we've written the fingerprints @ this key to disk
                    if(lsh2[v] == "wroteToDisk"):
                        # If so, read it
                        l2 = l2 + self.readFromDisk(v)
                    # Otherwise get list of keys normally
                    else:
                        l2 = l2 + lsh2[v]

            # Check if these fingerprints have been written to disk
            fps = lsh1[k]
            # If so, pull them all from disk
            if(fps == "wroteToDisk"):
                fps = self.readFromDisk(k)

            # Look at fingerprints at the key in lsh1, compare to fingerprints
            # in lsh2 that might match.
            for fp in fps:
                for fp2 in l2:
                    if set([fp[2], fp2[2]]) not in matched:
                        if self.compare_fprints(fp, fp2):
                            matched.append(set([fp[2], fp2[2]]))
                            self.print_match(fp, fp2)

    # compares two fingerprints, returns true if a match is found
    def compare_fprints(self, fp1, fp2):


        # value, will turn false if anything is found to be inconsistent
        val = True

        # check to see our amplitudes of frequency bands
        # are of similar value
        for i in range(5):
            bv1 = fp1[0][i]
            bv2 = fp2[0][i]

            # if band power values are zero, simply change them to number
            # very close to 0 for division purposes
            if bv1 == 0:
                bv1 = 0.000000001
            if bv2 == 0:
                bv2 = 0.000000001


            val = val and (.9 <= bv1/bv2 <= 1.1)

        # next, see if frequencies in the fingerprints are similar
        for i in range(6,10):

            fv1 = fp1[0][i]
            fv2 = fp2[0][i]

            # if frequencies are zero, simply change them to number very close
            # to 0 for division purposes
            if bv1 == 0:
                bv1 = 0.000000001
            if bv2 == 0:
                bv2 = 0.000000001

            val = val and (.9 <= fv1/fv2 <= 1.1)

        return val


    # this function returns a list of fingerprints for a given file
    def makeFingerprints(self, file):

        # Get a list of segments to be fingerprinted
        segList = Segmenter.segment_data(file[0])

        # array where fingerprints will be stored
        fprints = []

        # Go through this list of segments, converting each segment
        # in place into its corresponding fingerprint
        # conversions will be to a tuple of the form:
        # (fingerprint, time offset of that fingerprint, file name)
        for n in range(len(segList)):
            t = (self.fingerprint(segList[n][0]), segList[n][1], file[1])
            fprints.append(t)

        return fprints

    # compute a fingerprint for a given range of samples
    def fingerprint(self, samples, bands = BANDS):

        # take an fft over our samples and convert the complex values
        # to their magnitudes (only take positive frequencies, then normalize
        samples = list(fft(samples))
        samples = map(abs, samples[0:SAMPLES_PER_SEGMENT/2])
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
            top5.append(FREQS[samples.index(x)])

        top5 = sorted(top5)


        return fprint+top5


    # a hash function for our LSH tables, takes a fingerprint
    # and returns a hashvalue for that fingerprint
    def hashFunct(self, fprint):

        # the hash function will be a sequence of weights times
        # the band strengths plus the average of the strongest frequencies
        val = 0
        lw = len(WEIGHTS)
        for x in range(lw):
            val += WEIGHTS[x]*(fprint[0][x]/100.0)

        return int(val)

    # Write the given fingerprint to disk, naming the file after the hashkey
    # Append the hashkey to a list of things we've written to disk
    def writeToDisk(self, key, fingerprint, isList=False):
        # Get our current directory
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # Set our destination directory /tmp/
        dest_dir = os.path.join(cur_dir, 'tmp/lsh')
        # Try to make the tmp dir
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass  # Already exists
        # Create our target path
        path = os.path.join(dest_dir, str(key)+'.txt')
        # Write fingerprint to disk
        with open(path, 'a') as stream:  # Open file in append mode
            # if the fingerprint variable is actually a list, simply
            # make strings of all the fingerprints followed by newlines
            if isList:
                s = ""
                for x in fingerprint:
                    s = s + str(x) + "\n"
                stream.write(s)
            else:
                stream.write(str(fingerprint)+"\n")

        # Add hashkey to list of things we've written
        writtenToDisk.append(key)
        stream.close()

    # Given a hashkey, try to find the corresponding fingerprint txt file
    def readFromDisk(self, key):
        try:
            f = open('tmp/lsh/'+str(key)+".txt", 'r') # Open file in read mode
            readFile = f.read()
            listOfFingerprints = readFile.splitlines()
            return listOfFingerprints
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

        s = "MATCH: %s %s %s %s"

        # extract short names of our files
        fn1 = fp1[2].split('/')
        fn1 = fn1[len(fn1)-1]

        fn2 = fp2[2].split('/')
        fn2 = fn2[len(fn2)-1]

        # get times rounded to nearest tenth
        t1 = str(round(fp1[1], 1))
        t2 = str(round(fp2[1], 1))

        print (s % (fn1, fn2, t1, t2))

    # parse a string representation of a fingerprint
    # converting it into an actual fingerprint
    def parse_fprint_string(self, s):

        # split the fingerprint string along
        # occurances of ', '
        splitString = s.split(', ')

        fprint = []

        # go through the fingerprint numerical data
        # in the split up string, convert to floats
        for i in range(10):
            if i == 0:
                fprint.append(float(splitString[i][2:len(splitString[i])]))
            elif i == 9:
                fprint.append(float(splitString[i][0:len(splitString[i])-1]))
            else:
                fprint.append(float(splitString[i]))

        offset = float(splitString[10])

        name = splitString[11][1:len(splitString[11])-2]

        return (fprint, offset, name)
