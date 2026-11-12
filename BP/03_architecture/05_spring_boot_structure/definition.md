# Aplicación Spring Boot por responsabilidades

## ¿Qué es?

Es separar el controlador HTTP, el caso de uso y el adaptador de almacenamiento, conectándolos mediante inyección por constructor.

## ¿Cómo funciona y para qué sirve?

El dominio y OrderService no importan Spring. La configuración crea el bean y el repositorio implementa un puerto. Los DTO validan la entrada y un handler traduce errores conocidos.

## Qué muestra el ejemplo

Es un ejemplo pequeño completo: POST y GET /orders, validación de cantidades, repositorio limitado, pruebas unitarias y pruebas HTTP con puerto aleatorio. Actuator publica liveness y readiness.

Tecnología: **Spring Boot 3.5.16 y Java 21**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
cd .\BP\03_architecture\05_spring_boot_structure
mvn test
mvn spring-boot:run
```

## Qué pide la organización

Las pruebas reflejan los paquetes del código principal. Se usan JUnit, Mockito y pruebas HTTP reales. El reporte de JaCoCo queda en target/site/jacoco/index.html; no se impone un porcentaje sin aclarar su alcance.

## Límites y aclaraciones

No es el CRUD de producción ni un sistema autenticado. No usa PostgreSQL: SQL se estudia por separado. Las versiones elegidas permiten reproducir el ejercicio y no se presentan como homologación corporativa.

## Referencias

Consulta [spring](../../SOURCES.md#spring) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
