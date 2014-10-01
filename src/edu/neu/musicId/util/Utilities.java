
package edu.neu.musicId.util;

/**
 * This class contains various static utility methods.
 * 
 * @author ckolek
 * @since 1.0
 */
public final class Utilities {
    /** Size of 16-bit unsigned integer in bytes */
    public static final int UINT16_SIZE = Short.SIZE / Byte.SIZE;

    /** Size of 32-bit unsigned integer in bytes */
    public static final int UINT32_SIZE = Integer.SIZE / Byte.SIZE;

    /** Size of float in bytes */
    public static final int FLOAT_SIZE = Float.SIZE / Byte.SIZE;

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
    public static int toInt16(byte[] bytes, int offset, boolean unsigned, boolean isLittleEndian) {
        return (int) toInt(bytes, offset, UINT16_SIZE, unsigned, isLittleEndian);
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
    public static int toInt16(byte[] bytes, boolean unsigned, boolean isLittleEndian) {
        return toInt16(bytes, 0, unsigned, isLittleEndian);
    }

    /**
     * Extracts a 32-bit unsigned integer from the given array of
     * <code>byte</code>s offset at the given index.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param offset the offset from the beginning of the array to extract the
     *            value from
     * @param isLittleEndian if the value is stored in little-endian form
     * @return a <code>long</code> with the 32-bit unsigned integer value
     * @since 1.0
     */
    public static long toInt32(byte[] bytes, int offset, boolean unsigned, boolean isLittleEndian) {
        return toInt(bytes, offset, UINT32_SIZE, unsigned, isLittleEndian);
    }

    /**
     * Extracts a 32-bit unsigned integer from the given array of
     * <code>byte</code>s.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param isLittleEndian if the value is stored in little-endian form
     * @return a <code>long</code> with the 32-bit unsigned integer value
     * @since 1.0
     */
    public static long toInt32(byte[] bytes, boolean unsigned, boolean isLittleEndian) {
        return toInt32(bytes, 0, unsigned, isLittleEndian);
    }

    /**
     * Extracts a <code>length</code>-byte integer from the given array of
     * <code>byte</code>s offset at the given index.
     * 
     * @param bytes the array of <code>byte</code> values
     * @param offset
     * @param length
     * @param unsigned if the resulting value is unsigned
     * @param isLittleEndian if the value is stored in little-endian form
     * @return a <code>long</code> with the integer value
     * @since 1.0
     */
    public static long toInt(byte[] bytes, int offset, int length, boolean unsigned,
            boolean isLittleEndian) {
        long value = 0;

        for (int i = 0; i < length; i++) {
            byte b = isLittleEndian ? bytes[offset + i] : bytes[offset + (length - 1 - i)];

            if (unsigned) {
                value += (0xFF & b) << (Byte.SIZE * i);
            } else {
                value += b << (Byte.SIZE * i);
            }
        }

        return value;
    }
}
