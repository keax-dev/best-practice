// Tema: la API comunica errores conocidos sin enviar trazas internas.
package demo.bp.presentation;

import demo.bp.application.CapacityExceededException;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;

@RestControllerAdvice
public class ApiErrorHandler {
    public record ApiError(String code, String message) { }

    @ExceptionHandler({MethodArgumentNotValidException.class,
        HttpMessageNotReadableException.class, IllegalArgumentException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ApiError invalidInput(Exception error) {
        return new ApiError("INVALID_INPUT", "Quantity must be a positive integer");
    }

    @ExceptionHandler(CapacityExceededException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ApiError capacityReached(CapacityExceededException error) {
        return new ApiError("DEMO_CAPACITY_REACHED", "Demo capacity reached");
    }
}
