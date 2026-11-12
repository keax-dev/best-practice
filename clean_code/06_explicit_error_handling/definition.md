# Manejo explícito de errores

## ¿Qué es?

Es indicar claramente qué salió mal y manejar ese problema donde el programa
pueda decidir cómo responder.

Por ejemplo, si alguien escribe `coffee` como cantidad, no conviene devolver cero
y seguir como si fuera un dato correcto. La función puede lanzar un error de
cantidad inválida y el código que la llama puede mostrar un mensaje. Una
excepción es la forma en que Python comunica ese fallo mientras se ejecuta.

## Cuándo aporta

Al transformar entradas, leer recursos o ejecutar operaciones que pueden fallar.
Evita capturar `Exception` solo para esconder el problema o continuar sin saber
qué ocurrió.

## Qué muestra el ejemplo

`before.py` devuelve cero para cualquier excepción al interpretar una cantidad.
La demostración imprime cantidades de 3, 0 y 0: los dos últimos resultados ocultan
los problemas con `coffee` y `0`.

`after.py` define `InvalidQuantityError`. La conversión captura `ValueError` y
propaga un error de dominio conservando la causa con `raise ... from error`.
Una cantidad no positiva provoca otro mensaje del mismo error específico.

`main` decide cómo informar el problema al usuario:

```text
Quantity: 3
Invalid input: Quantity must be an integer
Invalid input: Quantity must be positive
```

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\06_explicit_error_handling\before.py
py -3.14 .\clean_code\06_explicit_error_handling\after.py
```

## Límite

Los type hints no impiden pasar valores de otro tipo en ejecución. El contrato
educativo de esta función recibe cadenas. Los errores inesperados no se capturan
como si fueran entradas inválidas. Una captura amplia puede ser apropiada en una
frontera de aplicación si registra el fallo y aplica una respuesta controlada.

Referencia: [errores y excepciones en Python](https://docs.python.org/3.14/tutorial/errors.html).
