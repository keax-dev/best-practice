# O: principio abierto/cerrado

## ¿Qué es?

Es preparar una parte del programa para agregar nuevas opciones sin tener que
reescribir la función que las utiliza.

Por ejemplo, cada modalidad de envío sabe calcular su tarifa. La función que
consulta esa tarifa trabaja igual con envío normal, exprés o retiro en tienda.
Al agregar una modalidad, creas su implementación y la eliges al preparar el
programa. Esto no significa que nunca puedas modificar el código existente.

## Cuándo aporta

Cuando una operación tiene modalidades que se amplían de forma recurrente, como
tarifas de envío o formas de notificación, y esas variantes pueden compartir un
contrato útil.

## Qué muestra el ejemplo

`before.py` calcula tarifas con condiciones sobre una cadena. Agregar un método
de envío obliga a editar `shipping_cost` y ampliar sus ramas.

`after.py` define `ShippingMethod.cost()`. `StandardShipping`, `ExpressShipping`
y `StorePickup` implementan ese contrato. `shipping_cost` solo llama a `cost`:
no necesita identificar cada tipo concreto.

Para añadir otra modalidad, crearías una implementación y la incluirías en la
composición de `main`. Ese punto de selección sí cambia; el consumidor permanece
estable. Ambas versiones imprimen tarifas de 5, 12 y 0 créditos.

## Ejecución desde la raíz

```powershell
py -3.14 .\solid\02_open_closed\before.py
py -3.14 .\solid\02_open_closed\after.py
```

## Límite

Si las modalidades son pocas y estables, un condicional o un diccionario puede
ser suficiente. La abstracción merece su coste cuando la extensión aporta valor.

Mecanismo utilizado: [clases abstractas de Python](https://docs.python.org/3.14/library/abc.html).
