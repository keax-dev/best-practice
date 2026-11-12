// Tema: el adaptador protege la colección y limita su tamaño dentro del proceso.
package demo.bp.infrastructure;

import demo.bp.application.CapacityExceededException;
import demo.bp.application.OrderRepository;
import demo.bp.domain.Order;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryOrderRepository implements OrderRepository {
    private static final int MAX_ORDERS = 100;
    private final List<Order> orders = new ArrayList<>();

    @Override
    public synchronized void save(Order order) {
        if (orders.size() >= MAX_ORDERS) {
            throw new CapacityExceededException();
        }
        orders.add(order);
    }

    @Override
    public synchronized List<Order> findAll() {
        return List.copyOf(orders);
    }
}
