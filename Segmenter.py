__author__ = 'Deniz'

import sys
from wave.waveData import WaveData
from wave.waveDataReader import WaveDataReader
from wave.waveDataFormat import WaveDataFormat
from util import utilities

class Segmenter:
    def segementData(wave):
        waveDataFormat1 = wave.get_wave_data_format()

        chunk = wave.chunk("data")

        data = getSamples(wave, waveDataFormat1, chunk)

        # Compute the size of a float in bytes (answer: 4)
        FLOAT_SIZE = 4

        # Compute the segmentation interval (in seconds)
        segmentInterval = getSegmentInterval(waveDataFormat1, chunk)

        # Compute the number of samples in each invterval by:
        # segment length * byterate / (number of bytes per sample)
        segmentInterval_numSamples = \
            (int)(segmentInterval * waveDataFormat1.getByteRate()) \
                  / waveDataFormat1.getBytesPerSample()

        # Compute the number of segments in this wave
        numSegments = (int)(data.length / segmentInterval_numSamples)

        # Init array of arrays with dimenions:
        # Num Segments LONG x Num samples per Segment WIDE
        segmentedData = [[float for i in range(numSegments)] for j in range(segmentInterval_numSamples)]

        # For every segment, declare a new array of doubles within
        # segmentedData[]][]
        for segmentIndex in xrange(numSegments):
            segmentedData[segmentIndex] = float[segmentInterval_numSamples]

            # For every sample in this segment, save it to the current
            # array of doubles within segmentedData[][]
            for sampleIndex in xrange(segmentInterval_numSamples):
                segmentedData[segmentIndex][sampleIndex] = data[sampleIndex]
                #print data[sampleIndex]

        return segmentedData

    def getSegmentInterval(self, format, chunk):
        return 1.0;

    def getSamples(self, wave, format, chunk):
        channels = chunk.extractChannels(format)

        bytesPerSample = format.getBytesPerSample()
        blockAlign = format.getBlockAlign()
        numSamples = chunk.length() / blockAlign
        divisor = Math.pow(2, 8 * bytesPerSample) - 1

        samples = float[numSamples]

        for i in xrange(samples.length):
            sample = 0

            for j in xrange(channels.length):
                sample += utilities.to_int(channels[j], (i * bytesPerSample),
                  bytesPerSample, (bytesPerSample < 2))
                # TODO: Does to_int not need the isLittleEndian arguement?

            samples[i] = (sample / (channels.length * divisor))

        return samples








