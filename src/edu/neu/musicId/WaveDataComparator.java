
package edu.neu.musicId;

import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveDataFormat;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.Segmenter;

public class WaveDataComparator {
    public boolean areMatching(WaveData wave1, WaveData wave2) {
        WaveDataFormat waveDataFormat1 = WaveDataFormat.fromWaveData(wave1);
        WaveDataFormat waveDataFormat2 = WaveDataFormat.fromWaveData(wave2);

        Chunk chunk1 = wave1.getChunk("data");
        Chunk chunk2 = wave2.getChunk("data");
        
        if (waveDataFormat1.getTime(chunk1) != waveDataFormat2.getTime(chunk2)) {
            return false;
        }
        
        // Segment both files TODO: Deniz's work here
        Segmenter segmenter = new Segmenter();

        float[][] wave1segments = segmenter.segmentData(wave1);
        float[][] wave2segments = segmenter.segmentData(wave2);

        // Do actual comparison TODO: Jeff's work here

        return true;
    }
}
