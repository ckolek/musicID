package edu.neu.musicId.exception;

import java.io.IOException;

/**
 * IOException subclass for invalid formats.
 * 
 * @author ckolek
 * @since 1.0
 */
public class InvalidFormatException extends IOException {
    private static final long serialVersionUID = 1L;

    public InvalidFormatException() {
        super();
    }

    public InvalidFormatException(String message) {
        super(message);
    }

    public InvalidFormatException(Throwable cause) {
        super(cause);
    }

    public InvalidFormatException(String message, Throwable cause) {
        super(message, cause);
    }
}
