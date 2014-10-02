
package edu.neu.musicId.util;

public final class Fourier {
    private Fourier() {

    }

    public static double[] fastTransform(double[] data) {
        if (data.length == 1) {
            return new double[] {
                data[0]
            };
        } else if ((data.length % 2) != 0) {
            throw new IllegalArgumentException("length of data must be a power of 2");
        }

        final int halfLength = data.length / 2;

        double[] even = new double[halfLength];
        double[] odd = new double[halfLength];

        for (int i = 0; i < halfLength; i++) {
            even[i] = data[2 * i];
            odd[i] = data[(2 * i) + 1];
        }

        even = fastTransform(even);
        odd = fastTransform(odd);

        double[] transformed = new double[data.length];

        for (int i = 0; i < halfLength; i++) {
            double value = even[i];
            double delta = odd[i] * Math.cos(-2 * i * Math.PI / data.length);

            transformed[i] = value + delta;
            transformed[halfLength + i] = value - delta;
        }

        return transformed;
    }
}
