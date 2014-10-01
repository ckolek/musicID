
package edu.neu.musicId.wav;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.junit.Test;

import edu.neu.musicId.wav.WaveData.Chunk;

public class WaveDataReaderTest {
    private static final short AUDIO_FORMAT = 1;
    private static final short NUM_CHANNELS = 2;
    private static final int SAMPLE_RATE = 44100;
    private static final short BITS_PER_SAMPLE = 16;

    private static final WaveDataStructure struct = new WaveDataStructure(AUDIO_FORMAT,
            NUM_CHANNELS, SAMPLE_RATE, BITS_PER_SAMPLE, new byte[0], true);

    @Test
    public void testRead() throws IOException {
        WaveDataReader reader = new WaveDataReader(getInputStream());

        WaveData wave;
        try {
            wave = reader.read();
        } finally {
            reader.close();
        }

        assertEquals("RIFF", wave.getChunkId());
        assertEquals(struct.getFmt().length + struct.getData().length, wave.getChunkSize());
        assertEquals("WAVE", wave.getFormat());

        WaveDataFormat format = wave.getWaveDataFormat();

        assertNotNull(format);

        assertEquals(AUDIO_FORMAT, format.getAudioFormat());
        assertEquals(NUM_CHANNELS, format.getNumChannels());
        assertEquals(SAMPLE_RATE, format.getSampleRate());
        assertEquals(SAMPLE_RATE * NUM_CHANNELS * BITS_PER_SAMPLE / 8, format.getByteRate());
        assertEquals(NUM_CHANNELS * BITS_PER_SAMPLE / 8, format.getBlockAlign());
        assertEquals(BITS_PER_SAMPLE, format.getBitsPerSample());

        Chunk dataChunk = wave.getChunk("data");

        assertNotNull(dataChunk);

        assertArrayEquals(struct.getAudioData(), dataChunk.getData());
    }

    private static InputStream getInputStream() {
        return new ByteArrayInputStream(struct.getWave());
    }
}
