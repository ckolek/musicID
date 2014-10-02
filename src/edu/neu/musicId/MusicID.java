
package edu.neu.musicId;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import edu.neu.musicId.exception.InvalidFormatException;
import edu.neu.musicId.wav.WaveData;
import edu.neu.musicId.wav.WaveDataReader;

public class MusicID {
    private final File file1;
    private final File file2;
    
    private MusicID(String filePath1, String filePath2) {
        this.file1 = new File(filePath1);
        this.file2 = new File(filePath2);
    }

    public int run() {
        WaveData wave1;
        try {
            wave1 = readWaveData(file1);
        } catch (InvalidFormatException e) {
            return error("%s is not a supported format", file1.getName());
        } catch (IOException e) {
            return error(e.getMessage());
        }
        
        WaveData wave2;
        try {
            wave2 = readWaveData(file2);
        } catch (InvalidFormatException e) {
            return error("%s is not a supported format", file2.getName());
        } catch (IOException e) {
            return error(e.getMessage());
        }
        
        WaveDataComparator comparator = new WaveDataComparator();

        if (comparator.areMatching(wave1, wave2)) {
            return output("MATCH %s %s", file1.getName(), file2.getName());
        } else {
            return output("NO MATCH");
        }
    }
    
    private static WaveData readWaveData(File file) throws IOException {
        InputStream inputStream = new FileInputStream(file);
        
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
    
    private static int output(String format, Object... args) {
        System.out.printf(format, args);
        
        return 0;
    }
    
    private static int error(String format, Object... args) {
        System.err.printf("ERROR: " + format, args);
        
        return -1;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            error("Incorrect command line parameters");

            return;
        }

        MusicID id = new MusicID(args[0], args[1]);
        id.run();
    }
}
