// Tema: el controlador convierte solicitudes HTTP en llamadas al caso de uso.
package demo.bp.presentation;

import demo.bp.application.OrderService;
import demo.bp.domain.Order;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@Valid @RequestBody OrderInput input) {
        return service.create(input.quantity());
    }

    @GetMapping
    public List<Order> list() {
        return service.list();
    }
}
