
package edu.neu.musicId.wav;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class WaveDataStructure {
    private final byte[] wave;
    private final byte[] fmt;
    private final byte[] data;
    private final byte[] audioData;

    public WaveDataStructure(short audioFormat, short numChannels, int sampleRate,
            short bitsPerSample, byte[] audioData, boolean isLittleEndian) {
        ByteOrder order = isLittleEndian ? ByteOrder.LITTLE_ENDIAN : ByteOrder.BIG_ENDIAN;

        ByteBuffer fmtBuffer = ByteBuffer.allocate(24);
        fmtBuffer.order(order);
        fmtBuffer.put("fmt ".getBytes());
        fmtBuffer.putInt(16);
        fmtBuffer.putShort(audioFormat);
        fmtBuffer.putShort(numChannels);
        fmtBuffer.putInt(sampleRate);
        fmtBuffer.putInt(sampleRate * numChannels * bitsPerSample / 8);
        fmtBuffer.putShort((short) (numChannels * bitsPerSample / 8));
        fmtBuffer.putShort(bitsPerSample);

        fmt = fmtBuffer.array();

        ByteBuffer audioDataBuffer = ByteBuffer.allocate(audioData.length);
        audioDataBuffer.order(order);
        audioDataBuffer.put(audioData);

        this.audioData = audioDataBuffer.array();

        ByteBuffer dataBuffer = ByteBuffer.allocate(8 + audioData.length);
        dataBuffer.order(order);
        dataBuffer.put("data".getBytes());
        dataBuffer.putInt(audioData.length);
        dataBuffer.put(audioData);

        data = dataBuffer.array();

        ByteBuffer waveBuffer = ByteBuffer.allocate(12 + fmt.length + data.length);
        waveBuffer.order(order);
        waveBuffer.put((isLittleEndian ? "RIFF" : "RIFX").getBytes());
        waveBuffer.putInt(fmt.length + data.length);
        waveBuffer.put("WAVE".getBytes());
        waveBuffer.put(fmt);
        waveBuffer.put(data);

        wave = waveBuffer.array();
    }

    public byte[] getWave() {
        return wave;
    }

    public byte[] getFmt() {
        return fmt;
    }

    public byte[] getData() {
        return data;
    }

    public byte[] getAudioData() {
        return audioData;
    }
}
