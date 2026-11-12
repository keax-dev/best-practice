// Tema: la integración pasa por HTTP real, deserialización, validación y servicio.
package demo.bp.presentation;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.*;
import org.springframework.test.context.ActiveProfiles;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class OrderHttpTest {
    @Autowired
    private TestRestTemplate http;

    @Test
    void invalidInputHasNoEffectAndValidInputCreatesOrder() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        for (String body : List.of("{\"quantity\":true}", "{\"quantity\":0}",
                "{\"quantity\":1.5}", "{\"quantity\":2,\"extra\":1}")) {
            ResponseEntity<Map> response = http.postForEntity("/orders", new HttpEntity<>(body, headers), Map.class);
            assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
            assertEquals("INVALID_INPUT", response.getBody().get("code"));
        }
        assertEquals(0, http.getForObject("/orders", List.class).size());
        ResponseEntity<Map> created = http.postForEntity("/orders", Map.of("quantity", 2), Map.class);
        assertEquals(HttpStatus.CREATED, created.getStatusCode());
        assertEquals(2, created.getBody().get("quantity"));
        assertEquals(1, http.getForObject("/orders", List.class).size());
    }

    @Test
    void healthGroupsAreAvailable() {
        assertEquals(HttpStatus.OK, http.getForEntity("/actuator/health/liveness", Map.class).getStatusCode());
        assertEquals(HttpStatus.OK, http.getForEntity("/actuator/health/readiness", Map.class).getStatusCode());
    }
}
