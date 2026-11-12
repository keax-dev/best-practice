// Tema: la regla recibe el repositorio por constructor, sin depender de Spring.
package demo.bp.application;

import demo.bp.domain.Order;
import java.util.List;
import java.util.UUID;

public class OrderService {
    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public Order create(int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        Order order = new Order(UUID.randomUUID(), quantity);
        repository.save(order);
        return order;
    }

    public List<Order> list() {
        return repository.findAll();
    }
}
