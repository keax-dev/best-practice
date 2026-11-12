# Nombres claros

## ¿Qué es?

Es elegir nombres que permitan entender para qué sirve una variable, una función
o una clase sin tener que adivinarlo.

Por ejemplo, `quantity` indica una cantidad y `calculate_order_total` indica que
la función calcula el total de un pedido. Nombres como `q` o `calc` obligan a
buscar más información para entender lo mismo.

En Python usamos normalmente `snake_case` para variables y funciones,
`CapWords` para clases y `UPPER_SNAKE_CASE` para constantes.

## Cuándo aporta

Al nombrar parámetros de negocio, funciones reutilizadas y valores que otras
personas necesitan interpretar. Evita abreviaturas locales que solo entiende
quien escribió el código.

## Qué muestra el ejemplo

En `before.py`, `calc(p, q, d)` no explica qué representan sus argumentos.
En `after.py`, `calculate_order_total(unit_price, quantity, discount_amount)`
expresa la operación y diferencia el descuento fijo de un porcentaje.

Ambas versiones calculan `25 * 4 - 10` y muestran:

```text
Order total: 90 credits
```

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\01_clear_naming\before.py
py -3.14 .\clean_code\01_clear_naming\after.py
```

## Límite

Más largo no significa más claro. Usa el contexto para evitar repeticiones.
Los nombres descriptivos tampoco sustituyen la validación de entradas.

Referencia: [convenciones de nombres en PEP 8](https://peps.python.org/pep-0008/#naming-conventions).
