__author__ = 'Deniz'

from wave.waveData import WaveData
from wave.waveDataFormat import WaveDataFormat

class WaveDataComparator:
    def areMatching(self, wave1, wave2):
        waveDataFormat1 = wave1.get_wave_data_format()
        waveDataFormat2 = wave2.get_wave_data_format()

        chunk1 = wave1.chunk("data")
        chunk2 = wave2.chunk("data")

        # Check if files are same length in time
        if(waveDataFormat1.get_Time(chunk1) != waveDataFormat2.get_Time(chunk2)):
            return false

        # Segment both files
        segmenter = Segmenter()

        wave1segments = segmenter.segmentData(wave1)
        wave2segments = segmenter.segmentData(wave2)

        # Do actual comparison of segments here
        return true