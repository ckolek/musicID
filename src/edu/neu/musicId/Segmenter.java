package edu.neu.musicId;

import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;
import edu.neu.musicId.util.Utilities;

import java.util.Arrays;

/**
 * Created by Deniz on 9/30/2014.
 */
public class Segmenter {
    public float[][] segmentFile(WaveData wave, float segmentInterval){
        float[][] segmentedFile = new float[][]{};

        WaveDataFormat waveDataFormat1 = WaveDataFormat.fromWaveData(wave);

        Chunk chunk = wave.getChunk("data");

        byte[] data = chunk.getData();

        // Populate the array of arrays of floats by calling the toFloat Utilities method
        // and incrementing the counter by 4
        for (int i = 0; i < data.length; i += 4) {
            Arrays.fill(segmentedFile, Utilities.toFloat(data, i, wave.isLittleEndian()));
        }

        System.out.println(segmentedFile);

        return segmentedFile;
    }

}
