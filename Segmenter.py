__author__ = 'Deniz'

from util import utilities

# duration of each segment of samples (in seconds)
SEGMENT_DURATION = 0.2

# sample rate to downsample audio to
TARGET_SAMPLE_RATE = 22050

# Segment the data in the given wav file
def segment_data(wave):
    format = wave.wave_data_format

    chunk = wave.chunk("data")

    downsample_factor = format.sample_rate / TARGET_SAMPLE_RATE

    sample_rate = format.sample_rate / downsample_factor
    byte_rate = format.byte_rate / downsample_factor

    samples_per_segment = int(SEGMENT_DURATION * byte_rate /
                              format.bytes_per_sample)

    num_samples = chunk.length() / format.block_align
    num_segments = num_samples / samples_per_segment / downsample_factor

    print "length: %d, block_align: %d" % (chunk.length(), format.block_align)
    print "sample_rate: %d, byte_rate: %d, downsample_factor: %d" % (sample_rate, byte_rate, downsample_factor)
    print "samples_per_segment: %d, num_samples: %d, num_segments: %d" % (samples_per_segment, num_samples, num_segments)

    if format.bytes_per_sample == 1:
        convert = utilities.to_byte
    elif format.bytes_per_sample == 2:
        convert = utilities.to_short
    else:
        convert = utilities.to_long

    is_unsigned = format.bytes_per_sample < 2

    time_step = float(samples_per_segment) / sample_rate

    segments = []

    for i in xrange(num_segments):
        samples = []

        for j in xrange(samples_per_segment / downsample_factor):
            sample = 0

            for k in xrange(format.num_channels):
                sample_offset = downsample_factor *\
                        (i * samples_per_segment + j)

                byte_offset = sample_offset * format.block_align +\
                        k * format.bytes_per_sample

                try:
                    sample += convert(chunk.data,
                                      byte_offset,
                                      is_unsigned,
                                      wave.is_little_endian)
                except:
                    print "sample_offset: %d, byte_offset: %d" % (sample_offset, byte_offset)
                    return

            samples.append(float(sample) / format.num_channels)

        segments.append((samples, samples_per_segment * time_step))

    return segments
