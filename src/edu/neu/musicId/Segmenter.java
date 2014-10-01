
package edu.neu.musicId;

import java.util.ArrayList;
import java.util.Arrays;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;

public class Segmenter {
    public float[][] segmentData(WaveData wave) {
        WaveDataFormat waveDataFormat1 = wave.getWaveDataFormat();

        Chunk chunk = wave.getChunk("data");

        float[] data = getSamples(wave, waveDataFormat1, chunk);

        // Computes the size of a float in bytes (answer: 4)
        final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;

        // Compute the segmentation interval (in seconds)
        final float segmentInterval = getSegmentInterval(waveDataFormat1, chunk);

        // Compute the number of samples in each segment interval by:
        // segment length * byterate / (number of bytes per sample)
        int segmentInterval_numSamples = (int) (segmentInterval * waveDataFormat1.getByteRate())
                / waveDataFormat1.getBytesPerSample();

        // Compute the number of segments in this wave
        int numSegments = (int) (segmentInterval_numSamples / waveDataFormat1.getTime(chunk));

        // Initialize array of arrays with dimensions:
        // Num Segments long x Num Samples per Segment wide
        float[][] segmentedData = new float[numSegments][segmentInterval_numSamples];

        // Declare temporary array and counters used by foreach loop
        float[] tempArray_floats = new float[segmentInterval_numSamples];

        int cnt = 0;
        int arrayIndex = 0;
        // For each sample in the data array, increment a counter cnt and add
        // the sample to a temporary array. If the counter reaches the
        // segmentInterval_numSamples value, add the temp array to the
        // segmentedData array of arrays. Empty the temp array, reset the
        // cnt counter, and increment the arrayIndex counter.
        for (float _float : data[arrayIndex]) {
            // If the counter has reached the segment interval
            if (cnt > segmentInterval_numSamples) {
                // Save the temp array of floats to segmentedData
                segmentedData[arrayIndex] = tempArray_floats;

                arrayIndex++; // Increment the array index

                // Empty the temp array
                tempArray_floats = new float[segmentInterval_numSamples];

                cnt = 0; // Reset counter
            }
            // Otherwise fill temp array with samples in this segment
            tempArray_floats[cnt] = _float;
            // Increment counter
            cnt++;
        }

        System.out.println(segmentedData);

        return segmentedData;
    }

    private static float getSegmentInterval(WaveDataFormat format, Chunk chunk) {
        return 1F;
    }

    private static float[] getSamples(WaveData wave, WaveDataFormat format, Chunk chunk) {
        byte[][] channels = chunk.extractChannels(format);

        final int bytesPerSample = format.getBytesPerSample();
        final int blockAlign = format.getBlockAlign();
        final int numSamples = chunk.length() / blockAlign;

        float[] samples = new float[numSamples];

        for (int i = 0; i < samples.length; i++) {
            float sample = 0;

            for (int j = 0; j < channels.length; j++) {
                sample += Utilities.toInt(channels[j], (i * blockAlign) + (j * bytesPerSample),
                        bytesPerSample, (bytesPerSample < 2), wave.isLittleEndian());
            }

            samples[i] = sample / channels.length;
        }

        return samples;
    }
}
