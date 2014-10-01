
package edu.neu.musicId.wav;

import edu.neu.musicId.util.Utilities;
import edu.neu.musicId.wav.WaveData.Chunk;

/**
 * This class represents the information found in the FMT chunk of a WAVE format
 * file.
 * 
 * @author ckolek
 * @since 1.0
 */
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

    /**
     * @return an <code>int</code> with a 16-bit unsigned integer value
     *         representing the WAVE audio format
     * @since 1.0
     */
    public int getAudioFormat() {
        return audioFormat;
    }

    /**
     * @return an <code>int</code> with a 16-bit unsigned integer value
     *         representing the number of channels in the WAVE audio data
     * @since 1.0
     */
    public int getNumChannels() {
        return numChannels;
    }

    /**
     * @return an <code>int</code> with a 32-bit unsigned integer value
     *         representing the sample rate (in Hz) of the WAVE audio
     * @since 1.0
     */
    public long getSampleRate() {
        return sampleRate;
    }

    /**
     * @return an <code>int</code> with a 32-bit unsigned integer value
     *         representing the byte rate (<code>sampleRate</code> x
     *         <code>numChannels</code> x <code>bitsPerSample</code>/8) of the
     *         WAVE audio data
     * @since 1.0
     */
    public long getByteRate() {
        return byteRate;
    }

    /**
     * @return an <code>int</code> with a 16-bit unsigned integer value
     *         representing the number of bytes for one WAVE audio sample
     *         including all channels (<code>numSamples</code> x
     *         <code>bitsPerSample</code>/8)
     * @since 1.0
     */
    public int getBlockAlign() {
        return blockAlign;
    }

    /**
     * @return an <code>int</code> with a 16-bit unsigned integer value
     *         representing the number of bits per sample of WAVE audio
     * @since 1.0
     */
    public int getBitsPerSample() {
        return bitsPerSample;
    }

    /**
     * @param chunk the {@link Chunk} to calculate the time of
     * @return the length of time (in seconds) of the data in the given
     *         {@code Chunk}
     * @since 1.0
     */
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

    /**
     * Retrieves the "fmt " {@link Chunk} from the given {@link WaveData} object
     * and creates a {@code WaveDataFormat} object from it.
     * 
     * @param waveData the {@code WaveData} object to create the
     *            {@code WaveDataFormat} object from
     * @return the new {@code WaveDataFormat} object, or <code>null</code> if
     *         the {@code WaveData} object does not contain a {@code Chunk} with
     *         the chunk ID "fmt "
     * @since 1.0
     */
    public static WaveDataFormat fromWaveData(WaveData waveData) {
        boolean isLittleEndian = waveData.isLittleEndian();

        Chunk fmtChunk = waveData.getChunk(CHUNK_ID__FMT);

        if (fmtChunk != null) {
            byte[] fmtData = fmtChunk.getData();

            return new WaveDataFormat(
                    Utilities.toInt16(fmtData, 0, isLittleEndian),
                    Utilities.toInt16(fmtData, 2, isLittleEndian),
                    Utilities.toInt32(fmtData, 4, isLittleEndian),
                    Utilities.toInt32(fmtData, 8, isLittleEndian),
                    Utilities.toInt16(fmtData, 12, isLittleEndian),
                    Utilities.toInt16(fmtData, 14, isLittleEndian));
        }

        return null;
    }
}
