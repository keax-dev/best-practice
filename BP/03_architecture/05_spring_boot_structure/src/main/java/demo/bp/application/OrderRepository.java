// Tema: el servicio expresa una capacidad sin conocer cómo se almacena.
package demo.bp.application;

import demo.bp.domain.Order;
import java.util.List;

public interface OrderRepository {
    void save(Order order);
    List<Order> findAll();
}
