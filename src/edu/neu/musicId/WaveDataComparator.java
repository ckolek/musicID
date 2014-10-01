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
        Chunk chunk2 = wave1.getChunk("data");
        if(waveDataFormat1.getTime(chunk1) != waveDataFormat2.getTime(chunk2)) {
            return false;
        }else {
            // Calculate the segment interval TODO: Chris' work here
            float segmentInterval = 1.0f;

            // Segment both files TODO: Deniz's work here
            Segmenter segmenter = new Segmenter();
            segmenter.segmentFile(wave1, segmentInterval);

            // Do actual comparison TODO: Jeff's work here

            return true;
        }
    }
}