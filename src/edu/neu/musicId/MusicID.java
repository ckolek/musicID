
package edu.neu.musicId;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveData.Chunk;
import edu.neu.musicId.wav.WaveDataFormat;
import edu.neu.musicId.wav.WaveDataReader;

public class MusicID {
    public static void main(String[] args) throws Exception {
        WaveData wave = readWaveData(args[0]);
        
        WaveDataFormat format = WaveDataFormat.fromWaveData(wave);
        
        System.out.println(wave);
        System.out.println(format);
        
        Chunk dataChunk = wave.getChunk("data");
        
        byte[] data = dataChunk.getData();
        
        int numChannels = format.getNumChannels();
        int channelLength = data.length / numChannels;
        
        /*
        byte[][] channels = new byte[numChannels][channelLength];
        
        for (int i = 0; i < channelLength; i++) {
            for (int j = 0; j < numChannels; j++) {
                channels[j][i] = data[(i * numChannels) + j];
            }
        }
        */
        
        byte[] combined = new byte[channelLength];
        
        for (int i = 0; i < channelLength; i++) {
            short value = 0;
            
            for (int j = 0; j < numChannels; j++) {
                value += data[(i * numChannels) + j];
            }
            
            combined[i] = (byte) (value / numChannels);
        }
    }
    
    private static WaveData readWaveData(String fileName) throws IOException {
        InputStream inputStream = new FileInputStream(fileName);
        
        WaveDataReader reader = null;
        
        try {
            reader = new WaveDataReader(inputStream);
            
            return reader.read();
        } finally {
            if (reader != null) {
                reader.close();
            }
        }
    }
}
