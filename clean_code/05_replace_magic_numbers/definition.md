# Reemplazar números mágicos

## ¿Qué es?

Es dar un nombre a un número cuando leerlo por sí solo no explica para qué sirve.
Ese número sin explicación se suele llamar número mágico.

Por ejemplo, `100` no dice por qué un envío pasa a ser gratuito. El nombre
`FREE_SHIPPING_THRESHOLD = 100` explica que es el importe mínimo para obtener
envío gratis. La regla hace lo mismo, pero ahora se entiende al leerla.

## Cuándo aporta

Cuando el mismo umbral, tarifa o límite aparece en varias operaciones, o cuando
leer un número no permite saber qué decisión de negocio codifica.

## Qué muestra el ejemplo

`before.py` usa directamente 100 y 5 al calcular el envío.
`after.py` los nombra como `FREE_SHIPPING_THRESHOLD` y
`STANDARD_SHIPPING_COST`.

El comportamiento permanece igual: un subtotal de 80 tiene un envío de 5
créditos, y subtotales de 100 y 150 tienen envío gratuito.

El cero permanece como literal porque representa de forma evidente la ausencia
de cargo. El objetivo es explicar las decisiones, no reemplazar todos los números
por nombres.

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\05_replace_magic_numbers\before.py
py -3.14 .\clean_code\05_replace_magic_numbers\after.py
```

## Límite

Una constante no vuelve configurable un valor por sí sola. Si una política debe
cambiar sin modificar código, necesita otro mecanismo de configuración. Las
mayúsculas son una convención de Python, no impiden reasignar la variable.
