package edu.neu.musicId;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;

/**
 * Created by Deniz on 9/30/2014.
 */
public class Segmenter {
    public float[][] segmentData(WaveData wave){
        WaveDataFormat waveDataFormat1 = WaveDataFormat.fromWaveData(wave);

        Chunk chunk = wave.getChunk("data");

        byte[] data = chunk.getData();

        final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;
        
        float[] floats = new float[data.length / FLOAT_SIZE];
        // Populate the array of arrays of floats by calling the toFloat Utilities method
        // and incrementing the counter by 4
        for (int i = 0; i < floats.length; i++) {
            floats[i] = Utilities.toFloat(data, FLOAT_SIZE * i, wave.isLittleEndian());
        }
        
        final float segmentInterval = getSegmentInterval(waveDataFormat1, chunk);
        
        float[][] segmentedData = new float[][]{};

        System.out.println(segmentedData);

        return segmentedData;
    }
    
    private static float getSegmentInterval(WaveDataFormat format, Chunk chunk) {
        return 1F;
    }
}
