
package edu.neu.musicId.wav;

import java.io.Closeable;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collection;

import edu.neu.musicId.util.Utilities;

public class WaveDataReader implements Closeable {
    private final InputStream inputStream;

    public WaveDataReader(InputStream inputStream) {
        this.inputStream = inputStream;
    }

    public WaveData read() throws IOException {
        byte[] chunkIdBuf = new byte[4];

        long length = inputStream.read(chunkIdBuf);

        if (length < chunkIdBuf.length) {
            throw new IOException("could not read chunk ID");
        }

        final String chunkId = new String(chunkIdBuf);

        final boolean isLittleEndian;
        if (chunkId.equals(WaveData.CHUNK_ID__RIFF)) {
            isLittleEndian = true;
        } else if (chunkId.equals(WaveData.CHUNK_ID__RIFX)) {
            isLittleEndian = false;
        } else {
            throw new IOException("invalid chunk ID: " + chunkId);
        }

        byte[] chunkSizeBuf = new byte[4];

        length = inputStream.read(chunkSizeBuf);

        if (length < chunkSizeBuf.length) {
            throw new IOException("could not read chunk size");
        }

        final long chunkSize = Utilities.toInt32(chunkSizeBuf, isLittleEndian);

        byte[] formatBuf = new byte[4];

        length = inputStream.read(formatBuf);

        if (length < formatBuf.length) {
            throw new IOException("could not read chunk format");
        }

        final String format = new String(formatBuf);

        if (!format.equals("WAVE")) {
            throw new IOException("invalid format: " + format);
        }

        Collection<WaveData.Chunk> chunks = new ArrayList<WaveData.Chunk>();
        
        while (length < chunkSize) {
            WaveData.Chunk chunk = readChunk(isLittleEndian);

            chunks.add(chunk);

            length += 8 + chunk.length();
        }

        if (length < chunkSize) {
            throw new IOException("did not read " + chunkSize + " bytes of chunk");
        }

        return new WaveData(chunkId, isLittleEndian, chunkSize, format, chunks);
    }

    private WaveData.Chunk readChunk(boolean isLittleEndian) throws IOException {
        byte[] chunkIdBuf = new byte[4];

        long length = inputStream.read(chunkIdBuf);

        if (length < chunkIdBuf.length) {
            throw new IOException("could not read sub-chunk ID");
        }

        final String chunkId = new String(chunkIdBuf);

        byte[] chunkSizeBuf = new byte[4];

        length = inputStream.read(chunkSizeBuf);

        if (length < chunkSizeBuf.length) {
            throw new IOException("could not read sub-chunk size");
        }

        final long chunkSize = Utilities.toInt32(chunkSizeBuf, isLittleEndian);

        byte[] data = new byte[(int) chunkSize];

        length = inputStream.read(data);

        if (length < chunkSize) {
            throw new IOException("did not read " + chunkSize + " bytes of sub-chunk");
        }

        return new WaveData.Chunk(chunkId, data);
    }

    @Override
    public void close() throws IOException {
        inputStream.close();
    }
}
