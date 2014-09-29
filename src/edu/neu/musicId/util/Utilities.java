
package edu.neu.musicId.util;

public class Utilities {
    private Utilities() {

    }

    public static int toInt16(byte[] bytes, int startIndex, boolean isLittleEndian) {
        return (int) toInt(bytes, startIndex, 2, isLittleEndian);
    }

    public static int toInt16(byte[] bytes, boolean isLittleEndian) {
        return (int) toInt16(bytes, 0, isLittleEndian);
    }

    public static long toInt32(byte[] bytes, int startIndex, boolean isLittleEndian) {
        return toInt(bytes, startIndex, 4, isLittleEndian);
    }

    public static long toInt32(byte[] bytes, boolean isLittleEndian) {
        return toInt32(bytes, 0, isLittleEndian);
    }

    private static long toInt(byte[] bytes, int startIndex, int length, boolean isLittleEndian) {
        long value = 0;

        for (int i = 0; i < length; i++) {
            byte b = isLittleEndian ? bytes[startIndex + i] : bytes[startIndex + (length - 1 - i)];

            value += (b << (8 * i));
        }

        return value;
    }
}
