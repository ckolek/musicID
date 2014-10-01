
package edu.neu.musicId.wav;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * This class represents the data stored in a WAVE format file. It contains the
 * header information, as well as the collection of {@link Chunk}s that are
 * stored in the WAVE.
 * 
 * @author ckolek
 * @since 1.0
 */
public class WaveData {
    public static final String CHUNK_ID__RIFF = "RIFF";
    public static final String CHUNK_ID__RIFX = "RIFX";

    private final String chunkId;
    private final boolean isLittleEndian;
    private final long chunkSize;
    private final String format;

    private final Map<String, Chunk> chunks;

    public WaveData(String chunkId, boolean isLittleEndian, long chunkSize, String format,
            Collection<Chunk> chunks) {
        this.chunkId = chunkId;
        this.isLittleEndian = isLittleEndian;
        this.chunkSize = chunkSize;
        this.format = format;

        this.chunks = new LinkedHashMap<String, Chunk>();

        for (Chunk chunk : chunks) {
            this.chunks.put(chunk.getId(), chunk);
        }
    }

    /**
     * @return the chunk ID of the WAVE master chunk
     * @since 1.0
     */
    public String getChunkId() {
        return chunkId;
    }

    /**
     * @return <code>true</code> if the data in the WAVE is stored in
     *         little-endian form, or <code>false</code> if it is stored in
     *         big-endian form
     * @since 1.0
     */
    public boolean isLittleEndian() {
        return isLittleEndian;
    }

    /**
     * @return the chunk size (in <code>byte</code>s) of the WAVE master chunk
     * @since 1.0
     */
    public long getChunkSize() {
        return chunkSize;
    }

    /**
     * @return the format <code>String</code> of the WAVE master chunk
     * @since 1.0
     */
    public String getFormat() {
        return format;
    }

    /**
     * @param id the chunk ID of the {@link Chunk} to retrieve
     * @return the {@code Chunk} with the given chunk ID
     * @since 1.0
     */
    public Chunk getChunk(String id) {
        return chunks.get(id);
    }

    @Override
    public String toString() {
        StringBuilder string = new StringBuilder();
        string.append("chunkId: ").append(chunkId).append("\n");
        string.append("chunkSize: ").append(chunkSize).append("\n");
        string.append("format: ").append(format).append("\n");
        string.append("chunks: ").append(chunks.keySet());

        return string.toString();
    }

    /**
     * This class represents a chunk of WAVE data.
     * 
     * @author ckolek
     * @since 1.0
     */
    public static class Chunk {
        private final String id;
        private final byte[] data;

        public Chunk(String id, byte[] data) {
            this.id = id;
            this.data = data;
        }

        /**
         * @return the chunk ID of this {@code Chunk}
         * @since 1.0
         */
        public String getId() {
            return id;
        }

        /**
         * @return the length (in <code>byte</code>s) of the data in this
         *         {@code Chunk}
         * @since 1.0
         */
        public int length() {
            return data.length;
        }

        /**
         * @return the data in this {@code Chunk}
         * @since 1.0
         */
        public byte[] getData() {
            return data;
        }
    }
}
