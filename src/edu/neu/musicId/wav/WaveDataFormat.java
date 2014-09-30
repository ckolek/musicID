package edu.neu.musicId.wav;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData.Chunk;

public class WaveDataFormat {
    private static final String CHUNK_ID__FMT = "fmt ";
    
    private final int audioFormat;
    private final int numChannels;
    private final long sampleRate;
    private final long byteRate;
    private final int blockAlign;
    private final int bitsPerSample;
    
    public WaveDataFormat(int audioFormat, int numChannels, long sampleRate, long byteRate,
            int blockAlign, int bitsPerSample) {
        this.audioFormat = audioFormat;
        this.numChannels = numChannels;
        this.sampleRate = sampleRate;
        this.byteRate = byteRate;
        this.blockAlign = blockAlign;
        this.bitsPerSample = bitsPerSample;
    }

    public int getAudioFormat() {
        return audioFormat;
    }

    public int getNumChannels() {
        return numChannels;
    }

    public long getSampleRate() {
        return sampleRate;
    }

    public long getByteRate() {
        return byteRate;
    }

    public int getBlockAlign() {
        return blockAlign;
    }

    public int getBitsPerSample() {
        return bitsPerSample;
    }
    
    public double getTime(Chunk chunk) {
        return chunk.length() / (double) byteRate;
    }
    
    @Override
    public String toString() {
        StringBuilder string = new StringBuilder();
        string.append("audioFormat: ").append(audioFormat).append(" (");
        
        switch (audioFormat) {
            case 1:
                string.append("PCM");
                break;
            default:
                string.append("Other");
                break;
        }
        
        string.append(")\n");
        string.append("numChannels: ").append(numChannels).append(" (");
        
        switch (numChannels) {
            case 1:
                string.append("Mono");
                break;
            case 2:
                string.append("Stereo");
                break;
            default:
                string.append("Other");
                break;
        }

        string.append(")\n");
        string.append("sampleRate: ").append(sampleRate).append(" Hz\n");
        string.append("byteRate: ").append(byteRate).append(" bytes/s\n");
        string.append("blockAlign: ").append(blockAlign).append("\n");
        string.append("bitsPerSample: ").append(bitsPerSample);
        
        return string.toString();
    }

    public static WaveDataFormat fromWaveData(WaveData waveData) {
        boolean isLittleEndian = waveData.isLittleEndian();
        
        Chunk fmtChunk = waveData.getChunk(CHUNK_ID__FMT);
        
        byte[] fmtData = fmtChunk.getData();
        
        return new WaveDataFormat(
                Utilities.toInt16(fmtData, 0, isLittleEndian),
                Utilities.toInt16(fmtData, 2, isLittleEndian),
                Utilities.toInt32(fmtData, 4, isLittleEndian),
                Utilities.toInt32(fmtData, 8, isLittleEndian),
                Utilities.toInt16(fmtData, 12, isLittleEndian),
                Utilities.toInt16(fmtData, 14, isLittleEndian));
    }
}
