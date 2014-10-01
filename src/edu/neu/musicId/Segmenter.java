package edu.neu.musicId;

import java.util.ArrayList;
import java.util.Arrays;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;

public class Segmenter {
    public float[][] segmentData(WaveData wave){
        WaveDataFormat waveDataFormat1 = wave.getWaveDataFormat();

        Chunk chunk = wave.getChunk("data");

        float[][] data = getSamples(wave, waveDataFormat1, chunk);

        // Computes the size of a float in bytes (answer: 4)
        final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;

        // Compute the segmentation interval (in seconds)
        final float segmentInterval = getSegmentInterval(waveDataFormat1, chunk);

        // Compute the number of samples in each segment interval by:
        // segment length * byterate / (number of bytes per sample)
        int segmentInterval_numSamples = (int)(segmentInterval * waveDataFormat1.getByteRate()) / waveDataFormat1.getBytesPerSample();

        // Compute the number of segments in this wave
        int numSegments = (int)(segmentInterval_numSamples / waveDataFormat1.getTime(chunk));

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
            if(cnt > segmentInterval_numSamples) {
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
    
    private static float[][] getSamples(WaveData wave, WaveDataFormat format, Chunk chunk) {
        byte[][] channels = chunk.extractChannels(format);

        final int bytesPerSample = format.getBytesPerSample();

        float[][] samples = new float[channels.length][];

        for (int i = 0; i < samples.length; i++) {
            byte[] channel = channels[i];

            final int numSamples = channel.length / bytesPerSample;

            float[] channelSamples = new float[numSamples];

            for (int j = 0; j < numSamples; j += bytesPerSample) {
                float value = Utilities.toInt(channel, j * bytesPerSample, bytesPerSample,
                        (bytesPerSample < 2), wave.isLittleEndian());

                // TODO: divide value by maximum sample value

                channelSamples[j] = value;
            }

            samples[i] = channelSamples;
        }

        return samples;
    }
}
