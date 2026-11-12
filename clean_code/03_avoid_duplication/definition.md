# Evitar duplicación: DRY

## ¿Qué es?

Es escribir una regla compartida en un solo lugar y reutilizarla donde haga falta.
DRY significa *Don't Repeat Yourself*, es decir, no te repitas.

Por ejemplo, si la tienda física y la tienda online aplican el mismo descuento,
ambas pueden llamar a una función que lo calcula. Si cambia esa regla, la
actualizas una sola vez y evitas olvidar alguna copia.

## Cuándo aporta

Cuando diferentes operaciones deben aplicar exactamente la misma política, y
olvidar una copia al modificarla produciría resultados inconsistentes.

## Qué muestra el ejemplo

`before.py` repite el descuento en los canales de venta online y de tienda.
Ambos descuentan 10 créditos cuando el subtotal alcanza 100.

`after.py` centraliza la política en `apply_discount`. Los dos canales la usan
porque comparten la misma regla de negocio. Conservamos las funciones de cada
canal para mostrar dónde se delega la decisión.

Para un subtotal de 80, ambos devuelven 80. Para 120, ambos devuelven 110.
Las salidas de las dos versiones coinciden.

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\03_avoid_duplication\before.py
py -3.14 .\clean_code\03_avoid_duplication\after.py
```

## Límite

Dos fragmentos parecidos no siempre representan la misma regla. Si las políticas
de ambos canales evolucionan de forma independiente, forzar su unión podría
crear acoplamiento. Extrae conocimiento compartido, no semejanzas accidentales.
