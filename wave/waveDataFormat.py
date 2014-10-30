__author__ = 'ckolek'

from util import utilities


class WaveDataFormat:
    """
    Represents the information stored in the "fmt " subchunk of WAVE data,
     including:
        - Audio Format (unsigned 16-bit integer)
            * 0x01 : PCM
            * Other values indicate some form of compression
        - Number of Channels (unsigned 16-bit integer)
            * 0x01 : Mono
            * 0x02 : Stereo
            * Etc.
        - Sample Rate (in Hz; unsigned 32-bit integer)
        - Byte Rate (in bytes/s; unsigned 32-bit integer)
            * Equivalent to <Sample Rate> x <Number of Channels>
                x <Bits Per Sample> / 8
        - Block Align (unsigned 16-bit integer)
            * Equivalent to <Number of Channels> x <Bits Per Sample> / 8
        - Bits Per Sample (unsigned 16-bit integer)
    """

    def __init__(self, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample):
        """
        :param audio_format: the Audio Format (unsigned 16-bit integer)
        :param num_channels: the Number of Channels (unsigned 16-bit integer)
        :param sample_rate: the Sample Rate (in Hz; unsigned 32-bit integer)
        :param byte_rate: the Byte Rate (in bytes/s; unsigned 32-bit integer)
        :param block_align: the Block Align (unsigned 16-bit integer)
        :param bits_per_sample: the Bits Per Sample (unsigned 16-bit integer)
        """

        self.audio_format = audio_format
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.byte_rate = byte_rate
        self.block_align = block_align
        self.bits_per_sample = bits_per_sample

    def get_bytes_per_sample(self):
        """
        :return: the bytes per sample
        """

        return self.bits_per_sample / 8

    bytes_per_sample = property(get_bytes_per_sample)

    def get_time(self, chunk):
        """
        :param chunk: the chunk (containing audio data) of which to calculate
         the length in time
        :return: the length in seconds of the given chunk
        """

        return chunk.length() / float(self.byte_rate)

    def from_wave_data(wave):
        """
        :param wave: the WaveData object to extract a WaveDataFormat object from
        :return: the WaveDataFormat object for the given WaveData object
        """

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