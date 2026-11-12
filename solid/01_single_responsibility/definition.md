# S: principio de responsabilidad única

## ¿Qué es?

Es separar tareas que pueden cambiar por motivos diferentes, para que un cambio
en una de ellas no obligue a modificar las otras.

Por ejemplo, calcular cuánto cuesta una factura y decidir cómo mostrarla son
tareas distintas. Si cambia el formato del recibo, no deberías necesitar tocar
el código que calcula el total. Una clase puede tener varios métodos si todos
ayudan a cumplir la misma responsabilidad.

## Cuándo aporta

Cuando modificar la presentación de un dato obliga a tocar sus reglas de cálculo,
o cuando una clase mezcla negocio, almacenamiento y comunicación. Separar esos
motivos permite modificar cada parte con menor impacto sobre las demás.

## Qué muestra el ejemplo

En `before.py`, `Invoice` calcula el total y decide el texto del recibo. Una regla
de precios y un cambio de formato terminan en la misma clase.

En `after.py`, `Invoice` conserva el cálculo e `InvoiceRenderer` construye el
texto. Ambas versiones reciben los precios 40 y 60 e imprimen:

```text
Invoice total: 100 credits
```

El cambio de diseño puede no alterar la salida: lo importante es qué parte
necesitarías modificar si cambian las reglas o el formato.

## Ejecución desde la raíz

```powershell
py -3.14 .\solid\01_single_responsibility\before.py
py -3.14 .\solid\01_single_responsibility\after.py
```

## Límite

No dividas clases solo por su tamaño. Agrupa lo que cambia junto y separa lo que
tiene motivos independientes para cambiar. Aquí el renderer hace visible el
principio; en un programa mínimo también podría bastar una función de formato.
