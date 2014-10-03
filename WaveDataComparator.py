__author__ = 'Deniz'

import Segmenter


class WaveDataComparator:
    def areMatching(self, wave1, wave2):
        waveDataFormat1 = wave1.wave_data_format
        waveDataFormat2 = wave2.wave_data_format

        chunk1 = wave1.chunk("data")
        chunk2 = wave2.chunk("data")

        # Check if files are same length in time
        if waveDataFormat1.get_time(chunk1) != waveDataFormat2.get_time(chunk2):
            return False

        wave1segments = Segmenter.segmentData(wave1)
        wave2segments = Segmenter.segmentData(wave2)

        # Do actual comparison of segments here
        return True