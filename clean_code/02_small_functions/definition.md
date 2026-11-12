# Funciones pequeñas y coherentes

## ¿Qué es?

Es escribir funciones que realicen una tarea fácil de identificar y separar las
otras tareas en funciones con nombres claros cuando eso facilite entenderlas.

Por ejemplo, una función puede validar los artículos, otra calcular sus precios
y otra preparar el recibo. Una función principal las llama en orden. La idea es
entender cada paso con facilidad, no cumplir un número fijo de líneas.

## Cuándo aporta

Cuando necesitas recorrer toda una función para distinguir validación, cálculo y
formato, o cuando repetir una operación obliga a copiar fragmentos del código.

## Qué muestra el ejemplo

`before.py` construye el recibo mientras valida los datos y calcula los totales.
`after.py` separa `validate_items`, `calculate_subtotal` y `format_receipt`.
`build_receipt` coordina esas operaciones en un orden visible.

`OrderItem` nombra los campos que antes ocupaban posiciones dentro de una tupla.
La validación sigue comprobando que haya artículos y que precio y cantidad sean
positivos. Ambas versiones generan:

```text
Receipt
Coffee: 10 credits
Tea: 3 credits
Total: 13 credits
```

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\02_small_functions\before.py
py -3.14 .\clean_code\02_small_functions\after.py
```

## Límite

No extraigas cada línea a una función. La separación debe dar un nombre útil a
una operación y facilitar entenderla o probarla. El ejemplo valida solo las
condiciones necesarias para estudiar esta separación.
