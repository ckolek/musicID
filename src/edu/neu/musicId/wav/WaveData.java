
package edu.neu.musicId.wav;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

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

    public String getChunkId() {
        return chunkId;
    }

    public boolean isLittleEndian() {
        return isLittleEndian;
    }

    public long getChunkSize() {
        return chunkSize;
    }

    public String getFormat() {
        return format;
    }

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

    public static class Chunk {
        private final String id;
        private final byte[] data;

        public Chunk(String id, byte[] data) {
            this.id = id;
            this.data = data;
        }

        public String getId() {
            return id;
        }

        public int length() {
            return data.length;
        }

        public byte[] getData() {
            return data;
        }
    }
}
