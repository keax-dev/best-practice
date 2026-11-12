// Tema: una prueba unitaria controla el repositorio y comprueba efectos relevantes.
package demo.bp.application;

import demo.bp.domain.Order;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class OrderServiceTest {
    @Test
    void createPositiveQuantitySavesOrder() {
        OrderRepository repository = mock(OrderRepository.class);
        OrderService service = new OrderService(repository);
        Order result = service.create(2);
        assertEquals(2, result.quantity());
        assertNotNull(result.id());
        verify(repository).save(result);
    }

    @Test
    void createZeroQuantityDoesNotSaveOrder() {
        OrderRepository repository = mock(OrderRepository.class);
        OrderService service = new OrderService(repository);
        assertThrows(IllegalArgumentException.class, () -> service.create(0));
        verifyNoInteractions(repository);
    }
}
