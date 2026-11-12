// Tema: comprobar aislamiento de colecciones y límite del adaptador en memoria.
package demo.bp.infrastructure;

import demo.bp.application.CapacityExceededException;
import demo.bp.domain.Order;
import java.util.UUID;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class InMemoryOrderRepositoryTest {
    @Test
    void returnedOrdersCannotModifyRepository() {
        InMemoryOrderRepository repository = new InMemoryOrderRepository();
        repository.save(new Order(UUID.randomUUID(), 2));
        assertThrows(UnsupportedOperationException.class, () -> repository.findAll().clear());
        assertEquals(1, repository.findAll().size());
    }

    @Test
    void rejectedOrderDoesNotExceedCapacity() {
        InMemoryOrderRepository repository = new InMemoryOrderRepository();
        IntStream.range(0, 100).forEach(index -> repository.save(new Order(UUID.randomUUID(), 1)));
        assertThrows(CapacityExceededException.class, () -> repository.save(new Order(UUID.randomUUID(), 1)));
        assertEquals(100, repository.findAll().size());
    }
}
