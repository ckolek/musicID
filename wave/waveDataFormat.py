__author__ = 'ckolek'

from util import utilities


class WaveDataFormat:
    def __init__(self, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample):
        self.audio_format = audio_format
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.byte_rate = byte_rate
        self.block_align = block_align
        self.bits_per_sample = bits_per_sample

    def get_bytes_per_sample(self):
        return self.bits_per_sample / 8

    bytes_per_sample = property(get_bytes_per_sample)

    def get_time(self, chunk):
        return chunk.length() / float(self.byte_rate)

    def from_wave_data(wave):
        fmt_chunk = wave.chunk("fmt ")

        if fmt_chunk is not None:
            is_little_endian = wave.is_little_endian
            fmt_data = fmt_chunk.data

            return WaveDataFormat(
                utilities.to_short(fmt_data, 0, True, is_little_endian),
                utilities.to_short(fmt_data, 2, True, is_little_endian),
                utilities.to_long(fmt_data, 4, True, is_little_endian),
                utilities.to_long(fmt_data, 8, True, is_little_endian),
                utilities.to_short(fmt_data, 12, True, is_little_endian),
                utilities.to_short(fmt_data, 14, True, is_little_endian)
            )
        else:
            return None
    from_wave_data = staticmethod(from_wave_data)