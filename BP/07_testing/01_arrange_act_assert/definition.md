# Preparar, ejecutar y verificar

## ¿Qué es?

Es escribir una prueba donde puedas distinguir los datos preparados, la operación y la comprobación del resultado.

## ¿Cómo funciona y para qué sirve?

AAA separa Arrange, Act y Assert. La prueba verifica una propiedad observable, no solo que una función haya sido llamada.

## Qué muestra el ejemplo

before.py y after.py tienen la misma operación: la mejora está en test_example.py, que comprueba el resultado y tiene nombres que explican el caso.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\01_arrange_act_assert\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\01_arrange_act_assert\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
