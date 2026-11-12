// Tema: la composición conecta el puerto y el servicio sin acoplar el negocio al framework.
package demo.bp.config;

import demo.bp.application.OrderRepository;
import demo.bp.application.OrderService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ServiceConfiguration {
    @Bean
    OrderService orderService(OrderRepository repository) {
        return new OrderService(repository);
    }
}
