# Mocks y stubs

## ¿Qué es?

Es sustituir una dependencia para controlar sus respuestas y comprobar interacciones importantes.

## ¿Cómo funciona y para qué sirve?

Un stub proporciona una respuesta conocida; un mock también permite verificar cómo se utilizó. No se consulta una API real en una prueba unitaria.

## Qué muestra el ejemplo

test_example.py usa unittest.mock para simular stock y verificar el identificador consultado.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\03_mocks_and_stubs\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\03_mocks_and_stubs\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
