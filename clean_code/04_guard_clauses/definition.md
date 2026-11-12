# Salidas tempranas: guard clauses

## ¿Qué es?

Es revisar al inicio de una función los casos que impiden continuar y salir
enseguida cuando ocurre alguno. También se conoce como salida temprana.

Por ejemplo: si el usuario está inactivo, devuelve ese resultado; si la cantidad
es inválida, devuelve el error correspondiente. Después de esas comprobaciones
queda el caso exitoso, sin varios `if` metidos uno dentro de otro.

## Cuándo aporta

Cuando varios niveles de `if` y `else` dificultan reconocer el caso exitoso de
una función. Se puede salir con `return` o lanzar una excepción, según su contrato.

## Qué muestra el ejemplo

`before.py` anida las condiciones de usuario activo, cantidad positiva y stock.
`after.py` devuelve primero los resultados de rechazo y deja `CONFIRMED` al final.

Ambas versiones mantienen esta prioridad:

1. `INACTIVE_USER` si el usuario está inactivo.
2. `INVALID_QUANTITY` si la cantidad no es positiva.
3. `INSUFFICIENT_STOCK` si no hay unidades suficientes.
4. `CONFIRMED` cuando todo es correcto.

La demostración ejecuta un caso de cada resultado, en ese mismo orden.

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\04_guard_clauses\before.py
py -3.14 .\clean_code\04_guard_clauses\after.py
```

## Límite

Preserva el orden de evaluación y los efectos del código original. Una
refactorización que cambia qué validación tiene prioridad puede cambiar el
comportamiento aunque parezca equivalente.

Referencia: [catálogo de refactorización de Martin Fowler](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html).
