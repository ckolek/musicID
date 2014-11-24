__author__ = 'Deniz'

from util import utilities

# duration of each segment of samples (in seconds)
SEGMENT_DURATION = 0.2

# Segment the data in the given wav file
def segment_data(wave):
    format = wave.wave_data_format

    chunk = wave.chunk("data")

    samples_per_segment = int(SEGMENT_DURATION * format.byte_rate /
                              format.bytes_per_sample)

    num_samples = chunk.length() / format.block_align

    if format.bytes_per_sample == 1:
        convert = utilities.to_byte
    elif format.bytes_per_sample == 2:
        convert = utilities.to_short
    else:
        convert = utilities.to_long

    is_unsigned = format.bytes_per_sample < 2

    time_step = float(samples_per_segment)/format.sample_rate

    segments = []
    segment = []

    for i in xrange(num_samples):
        sample = 0

        for j in xrange(format.num_channels):
            sample += convert(chunk.data,
                              (i * format.block_align) +
                              (j * format.bytes_per_sample),
                              is_unsigned,
                              wave.is_little_endian)

        segment.append(sample / format.num_channels)

        if (len(segment) >= samples_per_segment):
            segments.append((segment, len(segments) * time_step))
            segment = []

    return segments
