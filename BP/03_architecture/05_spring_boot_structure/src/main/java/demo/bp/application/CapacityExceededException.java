// Tema: un error específico comunica el límite educativo de almacenamiento.
package demo.bp.application;

public class CapacityExceededException extends RuntimeException {
    public CapacityExceededException() {
        super("Demo order capacity reached");
    }
}
