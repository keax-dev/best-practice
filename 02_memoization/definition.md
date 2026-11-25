# Memoización

## ¿Qué es?

Guardar el resultado de una función para reutilizarlo cuando se repitan sus argumentos.

## ¿Cómo funciona?

`functools.lru_cache` identifica las llamadas por sus argumentos y conserva sus
resultados. `maxsize` limita las entradas; `cache_info()` permite observar su uso.

## ¿Cuándo usarla?

En cálculos repetidos cuyo resultado depende únicamente de sus argumentos.

## ¿Cuándo evitarla?

En funciones con efectos secundarios o resultados que cambian sin cambiar los
argumentos. No se deben memoizar directamente funciones asíncronas ni generadores.

## ¿Cómo aplicarla?

Usa argumentos hashables, como enteros, y resultados inmutables. Define una
capacidad y utiliza `cache_clear()` cuando corresponda. No incluye TTL y puede
repetir el cálculo ante misses concurrentes.

## Ejemplo práctico

Ejecuta `py -3.14 .\02_memoization\example.py`.
Dos cálculos iguales producen un miss y un hit; después se vacía la caché.

**Referencia:** [functools.lru_cache](https://docs.python.org/3.14/library/functools.html#functools.lru_cache).
