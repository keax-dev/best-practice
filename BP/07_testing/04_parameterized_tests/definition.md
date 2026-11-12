# Pruebas parametrizadas

## ¿Qué es?

Es ejecutar la misma regla con varios datos sin copiar la prueba ni esconder los casos dentro de un bucle.

## ¿Cómo funciona y para qué sirve?

pytest.mark.parametrize genera un caso independiente por entrada y muestra cuál falla.

## Qué muestra el ejemplo

La prueba parametriza enteros, cero, negativos, booleanos, texto y nulos. Cada caso tiene su propia comprobación.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\04_parameterized_tests\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\04_parameterized_tests\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
