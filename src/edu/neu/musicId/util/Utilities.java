
package edu.neu.musicId.util;

/**
 * This class contains various static utility methods.
 * 
 * @author ckolek
 * @since 1.0
 */
public final class Utilities {
    private Utilities() {

    }

    /**
     * Extracts a 16-bit unsigned integer from the given array of
     * <code>byte</code>s offset at the given index.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param offset the offset from the beginning of the array to extract the
     *            value from
     * @param isLittleEndian if the value is stored in little-endian form
     * @return an <code>int</code> with the 16-bit unsigned integer value
     * @since 1.0
     */
    public static int toInt16(byte[] bytes, int offset, boolean isLittleEndian) {
        return (int) toInt(bytes, offset, Short.SIZE / Byte.SIZE, isLittleEndian);
    }

    /**
     * Extracts a 16-bit unsigned integer from the given array of
     * <code>byte</code>s.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param isLittleEndian if the value is stored in little-endian form
     * @return an <code>int</code> with the 16-bit unsigned integer value
     * @since 1.0
     */
    public static int toInt16(byte[] bytes, boolean isLittleEndian) {
        return toInt16(bytes, 0, isLittleEndian);
    }

    /**
     * Extracts a 32-bit unsigned integer from the given array of
     * <code>byte</code>s offset at the given index.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param offset the offset from the beginning of the array to extract the
     *            value from
     * @param isLittleEndian if the value is stored in little-endian form
     * @return an <code>int</code> with the 32-bit unsigned integer value
     * @since 1.0
     */
    public static long toInt32(byte[] bytes, int offset, boolean isLittleEndian) {
        return toInt(bytes, offset, Integer.SIZE / Byte.SIZE, isLittleEndian);
    }

    /**
     * Extracts a 32-bit unsigned integer from the given array of
     * <code>byte</code>s.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param isLittleEndian if the value is stored in little-endian form
     * @return an <code>int</code> with the 32-bit unsigned integer value
     * @since 1.0
     */
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

    /**
     * Extracts a <code>float</code> from the given array of <code>byte</code>s
     * offset at the given index.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param offset the offset from the beginning of the array to extract the
     *            value from
     * @param isLittleEndian if the value is stored in little-endian form
     * @return the <code>float</code> value
     * @since 1.0
     */
    public static float toFloat(byte[] bytes, int offset, boolean isLittleEndian) {
        return Float.intBitsToFloat((int) toInt(bytes, offset, Float.SIZE / Byte.SIZE,
                isLittleEndian));
    }

    /**
     * Extracts a <code>float</code> from the given array of <code>byte</code>s.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param isLittleEndian if the value is stored in little-endian form
     * @return the <code>float</code> value
     * @since 1.0
     */
    public static float toFloat(byte[] bytes, boolean isLittleEndian) {
        return toFloat(bytes, 0, isLittleEndian);
    }
}
