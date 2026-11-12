# Errores y valores límite

## ¿Qué es?

Es probar los bordes de una regla y comprobar los fallos esperados, además del caso exitoso.

## ¿Cómo funciona y para qué sirve?

Si el descuento empieza en 100, prueba 99, 100 y 101. Para errores, comprueba el tipo de excepción y un mensaje útil.

## Qué muestra el ejemplo

La regla ficticia descuenta diez créditos desde 100 inclusive. La prueba comprueba ambos lados del límite y el valor negativo.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\05_error_and_boundary_cases\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\05_error_and_boundary_cases\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
