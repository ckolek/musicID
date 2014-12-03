__author__ = 'Deniz'

from util import utilities

# duration of each segment of samples (in seconds)
SEGMENT_DURATION = 0.2

# sample rate to downsample audio to
TARGET_SAMPLE_RATE = 22050

class Segmenter:
    def __init__(self):
        self.debug = False

    # Segment the data in the given wav file
    def segment_data(self, wave):
        format = wave.wave_data_format

        chunk = wave.chunk("data")

        # calculate the factor to downsample by
        downsample_factor = format.sample_rate / TARGET_SAMPLE_RATE

        sample_rate = format.sample_rate / downsample_factor
        byte_rate = format.byte_rate / downsample_factor

        samples_per_segment = int(SEGMENT_DURATION * byte_rate /
                                  format.bytes_per_sample)

        num_samples = chunk.length() / format.block_align
        num_segments = num_samples / samples_per_segment / downsample_factor
        
        if self.debug:
            print "\tlength: %d, block_align: %d" % (chunk.length(), format.block_align)
            print "\tsample_rate: %d, byte_rate: %d, downsample_factor: %d" % (sample_rate, byte_rate, downsample_factor)
            print "\tsamples_per_segment: %d, num_samples: %d, num_segments: %d" % (samples_per_segment, num_samples, num_segments)

        # determine the utility function to use to convert byte arrays to
        #  integer valus
        if format.bytes_per_sample == 1:
            convert = utilities.to_byte
        elif format.bytes_per_sample == 2:
            convert = utilities.to_short
        else:
            convert = utilities.to_long

        is_unsigned = format.bytes_per_sample < 2

        time_step = float(samples_per_segment) / sample_rate

        segments = []

        # create the segments
        for i in xrange(num_segments):
            samples = []

            for j in xrange(samples_per_segment / downsample_factor):
                sample = 0

                # create a mono sample
                for k in xrange(format.num_channels):
                    sample_offset = downsample_factor *\
                            (i * samples_per_segment + j)

                    byte_offset = sample_offset * format.block_align +\
                            k * format.bytes_per_sample

                    sample += convert(chunk.data,
                                      byte_offset,
                                      is_unsigned,
                                      wave.is_little_endian)

                samples.append(float(sample) / format.num_channels)

            segments.append((samples, len(segments) * time_step))

        return segments
