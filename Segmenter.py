__author__ = 'Deniz'

from util import utilities


def segment_data(wave):
    format = wave.wave_data_format

    chunk = wave.chunk("data")

    samples = get_samples(wave, format, chunk)

    segment_interval = get_segment_interval(wave, format, chunk)

    samples_per_segment = int(segment_interval * format.byte_rate / format.bytes_per_sample)

    num_segments = int(len(samples) / samples_per_segment)

    segments = []

    for i in xrange(num_segments):
        start = i * samples_per_segment
        end = start + samples_per_segment

        segments.append(samples[start:end])

    return segments


def get_segment_interval(wave, format, chunk):
        return 1.0;


def get_samples(wave, format, chunk):
    num_samples = chunk.length() / format.block_align
    divisor = float(2 ** (8 * format.bytes_per_sample) - 1)

    samples = []

    for i in xrange(num_samples):
        sample = 0

        for j in xrange(format.num_channels):
            sample += utilities.to_integer(chunk.data,
                                           format.bytes_per_sample,
                                           (i * format.block_align) + (j * format.bytes_per_sample),
                                           (format.bytes_per_sample < 2),
                                           wave.is_little_endian)

        samples.append(sample / (format.num_channels * divisor))

    return samples