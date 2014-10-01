package edu.neu.musicId;

import java.util.ArrayList;
import java.util.Arrays;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;

/**
 * Created by Deniz on 9/30/2014.
 */
public class Segmenter {
    public ArrayList<float[]> segmentData(WaveData wave){
        WaveDataFormat waveDataFormat1 = wave.getWaveDataFormat();

        Chunk chunk = wave.getChunk("data");

        byte[] data = chunk.getData();

        // Computes the size of a float in bytes (answer: 4)
        final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;

        // Compute the segmentation interval (in seconds)
        final float segmentInterval = getSegmentInterval(waveDataFormat1, chunk);

        // Compute the number of bytes in each segment interval by multiplying
        // the segment length * byterate
        float segmentInterval_numBytes = segmentInterval * waveDataFormat1.getByteRate();

        //float[][] segmentedData = new float[][]{};
        ArrayList<float[]> segmentedData = new ArrayList<float[]>();

        // Declare temporary arrays and counters used by foreach loop
        byte[] tempArray_bytes = new byte[]{};
        float[] tempArray_floats = new float[]{};

        float cnt = 0;
        int arrayIndex = 0;
        // For each byte in the data array, increment a counter and add the
        // byte to a temporary array. If the counter reaches the
        // segmentInterval_inBytes value, covert that temp array to floats, add
        // that array to the segmentedData array of arrays. Lastly empty out
        // the temp array and reset the counter.
        // TODO: If the Utilities.toFloat arguements are changed to float instead of float[] (or allow both?) it could
        // TODO: make this foreach more efficient. Instead of populating an array of bytes then converting that entire
        // TODO: array to an array of floats, we could convert each byte to a float and populate just 1 temp array
        for (byte _byte : data) {
            // If the counter has reached the segment interval
            if(cnt > segmentInterval_numBytes) {
                // Convert the temp array of bytes to floats and save results to temp array of floats
                for (int i = 0; i < tempArray_bytes.length; i++){
                    tempArray_floats[i] = Utilities.toFloat(tempArray_bytes, FLOAT_SIZE * arrayIndex, wave.isLittleEndian());
                }
                // Save the temp array of floats to segmentedData array of arrays
                segmentedData.add(arrayIndex, tempArray_floats);

                arrayIndex++; // Increment the array index

                // Empty temp arrays
                tempArray_bytes = new byte[]{};
                tempArray_floats = new float[]{};

                cnt = 0; // Reset counter

            }
            // Otherwise:
            // Fill this array with these bytes
            Arrays.fill(tempArray_bytes, _byte);
            // Increment counter
            cnt++;
        }

        System.out.println(segmentedData);

        return segmentedData;
    }
    
    private static float getSegmentInterval(WaveDataFormat format, Chunk chunk) {
        return 1F;
    }
}
