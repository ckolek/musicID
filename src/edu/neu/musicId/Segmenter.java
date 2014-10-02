
package edu.neu.musicId;

import java.util.ArrayList;
import java.util.Arrays;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;

public class Segmenter {
    public double[][] segmentData(WaveData wave) {
        WaveDataFormat waveDataFormat1 = wave.getWaveDataFormat();

        Chunk chunk = wave.getChunk("data");

        double[] data = getSamples(wave, waveDataFormat1, chunk);

        // Computes the size of a float in bytes (answer: 4)
        final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;

        // Compute the segmentation interval (in seconds)
        final double segmentInterval = getSegmentInterval(waveDataFormat1, chunk);

        // Compute the number of samples in each segment interval by:
        // segment length * byterate / (number of bytes per sample)
        int segmentInterval_numSamples = (int) (segmentInterval * waveDataFormat1.getByteRate())
                / waveDataFormat1.getBytesPerSample();

        // Compute the number of segments in this wave
        int numSegments = (int)(data.length / segmentInterval_numSamples);

        // Initialize array of arrays with dimensions:
        // Num Segments long x Num Samples per Segment wide
        double[][] segmentedData = new double[numSegments][segmentInterval_numSamples];

        // Declare temporary array and counters used by foreach loop
        double[] tempArray_doubles = new double[segmentInterval_numSamples];

        // TODO: Re-write for loop here using new getSamples() -Deniz

        System.out.println(segmentedData);

        return segmentedData;
    }

    private static double getSegmentInterval(WaveDataFormat format, Chunk chunk) {
        return 1F;
    }

    public static double[] getSamples(WaveData wave, WaveDataFormat format, Chunk chunk) {
        byte[][] channels = chunk.extractChannels(format);

        final int bytesPerSample = format.getBytesPerSample();
        final int blockAlign = format.getBlockAlign();
        final int numSamples = chunk.length() / blockAlign;
        final double divisor = Math.pow(2, 8 * bytesPerSample) - 1;

        double[] samples = new double[numSamples];

        for (int i = 0; i < samples.length; i++) {
            long sample = 0;

            for (int j = 0; j < channels.length; j++) {
                sample += Utilities.toInt(channels[j], (i * bytesPerSample), bytesPerSample,
                        (bytesPerSample < 2), wave.isLittleEndian());
            }
            
            samples[i] = (sample / (channels.length * divisor));
        }

        return samples;
    }
}
