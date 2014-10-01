
package edu.neu.musicId.util;

public final class Utilities {
    private Utilities() {

    }

    public static int toInt16(byte[] bytes, int offset, boolean isLittleEndian) {
        return (int) toInt(bytes, offset, Short.SIZE / Byte.SIZE, isLittleEndian);
    }

    public static int toInt16(byte[] bytes, boolean isLittleEndian) {
        return toInt16(bytes, 0, isLittleEndian);
    }

    public static long toInt32(byte[] bytes, int offset, boolean isLittleEndian) {
        return toInt(bytes, offset, Integer.SIZE / Byte.SIZE, isLittleEndian);
    }

    public static long toInt32(byte[] bytes, boolean isLittleEndian) {
        return toInt32(bytes, 0, isLittleEndian);
    }

    private static long toInt(byte[] bytes, int offset, int length, boolean isLittleEndian) {
        long value = 0;

        for (int i = 0; i < length; i++) {
            byte b = isLittleEndian ? bytes[offset + i] : bytes[offset + (length - 1 - i)];

            value += (0xFF & b) << (Byte.SIZE * i);
        }

        return value;
    }

    public static float toFloat(byte[] bytes, int offset, boolean isLittleEndian) {
        return Float.intBitsToFloat((int) toInt(bytes, offset, Float.SIZE / Byte.SIZE,
                isLittleEndian));
    }

    public static float toFloat(byte[] bytes, boolean isLittleEndian) {
        return toFloat(bytes, 0, isLittleEndian);
    }
}
