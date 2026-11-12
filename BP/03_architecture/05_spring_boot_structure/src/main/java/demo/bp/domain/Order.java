// Tema: el dato de negocio no necesita anotaciones web ni persistencia.
package demo.bp.domain;

import java.util.UUID;

public record Order(UUID id, int quantity) { }
