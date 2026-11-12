# Pruebas de integración

## ¿Qué es?

Es comprobar que varias partes trabajan juntas, por ejemplo rutas HTTP, validación y servicio.

## ¿Cómo funciona y para qué sirve?

El cliente de pruebas de Flask ejecuta el recorrido HTTP de la aplicación en memoria. No necesita abrir un puerto ni llamar a servicios productivos.

## Qué muestra el ejemplo

La prueba crea dos instancias de la aplicación y verifica creación, datos inválidos y aislamiento. El ejemplo Spring Boot tiene además una prueba HTTP sobre un puerto aleatorio.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\06_integration_tests\example.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Una llamada directa al método de un controlador no verifica por sí sola serialización, filtros y enrutamiento HTTP.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
