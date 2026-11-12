# L: principio de sustitución de Liskov

## ¿Qué es?

Es poder usar una clase hija en lugar de su clase base sin que el código que la
usa deje de funcionar como esperaba.

Por ejemplo, si el programa pide a una figura su área, todas las figuras deben
responder con un área correcta. Si además les exige cambiar ancho y alto por
separado, un cuadrado no puede cumplir esa petición manteniendo sus lados iguales.
Por eso no basta con heredar: la clase hija debe respetar lo que promete la base.

## Cuándo aporta

Al diseñar herencia o implementaciones de un mismo contrato. Revisa qué espera
el consumidor: resultados, condiciones aceptadas y efectos de cada operación.

## Qué muestra el ejemplo

En `before.py`, `Rectangle.resize(4, 5)` promete establecer ambos valores y dejar
un área de 20. `Square` mantiene lados iguales e ignora el alto solicitado.
Al sustituir el rectángulo por el cuadrado aparece el problema:

```text
Expected area: 20; actual area: 20
Expected area: 20; actual area: 16
```

En `after.py`, ambas figuras implementan `Shape.area()`. El rectángulo conserva
ancho y alto; el cuadrado conserva un lado. El consumidor `total_area` solo pide
el contrato que ambas figuras pueden cumplir. Imprime áreas de 20 y 16, y un
total de 36.

No se conserva una operación genérica de redimensionar: se corrige precisamente
ese contrato incompatible. La relación matemática entre figuras no obliga a
modelar herencia entre objetos mutables.

## Ejecución desde la raíz

```powershell
py -3.14 .\solid\03_liskov_substitution\before.py
py -3.14 .\solid\03_liskov_substitution\after.py
```

## Límite

Una clase abstracta ayuda a expresar métodos requeridos, pero no demuestra que
se cumplan sus condiciones. Las pruebas deben verificar también el comportamiento.
