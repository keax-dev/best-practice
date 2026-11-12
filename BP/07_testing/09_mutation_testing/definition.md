# Pruebas de mutación

## ¿Qué es?

Es introducir un cambio pequeño en el comportamiento y comprobar si las pruebas descubren ese error.

## ¿Cómo funciona y para qué sirve?

El mutante cambia >= por > en el umbral de descuento. Una prueba que no toca el límite puede seguir pasando aunque la regla esté rota.

## Qué muestra el ejemplo

La versión anterior deja sobrevivir al mutante; incluir 100 lo detecta. La prueba verifica que los casos también acepten la implementación original.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\09_mutation_testing\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\09_mutation_testing\after.py
```

## Qué pide la organización

La documentación menciona un mínimo del 60 % de cobertura de mutación para los stacks indicados. No equivale a cobertura de líneas ni implica homologar una herramienta Python.

## Límites y aclaraciones

Es una simulación determinista de un mutante, no un motor completo de mutación ni una medición de toda la aplicación. El manual homologa herramientas concretas para Java y .NET, no esta demostración Python.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
