// Tema: el DTO de entrada valida el contrato HTTP antes de ejecutar negocio.
package demo.bp.presentation;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public record OrderInput(@NotNull @Min(1) Integer quantity) { }
