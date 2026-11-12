# Comentarios útiles

## ¿Qué es?

Es usar comentarios para explicar por qué el código toma una decisión o sigue
una regla que no resulta evidente al leerlo.

Por ejemplo, un comentario puede aclarar que una cancelación se permite hasta
el séptimo día inclusive porque esa es la política del ejemplo. En cambio,
escribir «resta dos fechas» junto a una resta solo repite lo que el código ya
muestra. Los nombres claros ayudan a explicar qué hace cada operación.

## Cuándo aporta

Al explicar una política de negocio, una condición límite o una solución
necesaria por un comportamiento externo. No conviene narrar cada instrucción.

## Qué muestra el ejemplo

En `before.py`, los comentarios dicen que se restan fechas y se compara un
intervalo. Repiten lo que ya muestra la expresión, sin explicar de dónde sale 7.

En `after.py`, `elapsed_days` y `MAX_CANCELLATION_DAYS` explican los valores.
Los comentarios aclaran que la política ficticia permite cancelar hasta el
séptimo día inclusive, usa días calendario y rechaza fechas anteriores a la compra.
No se trata de una regla legal ni de una política de una empresa real.

Ambas versiones usan fechas fijas para que el resultado no dependa del día de
ejecución: el 1 y el 8 de enero de 2026 devuelven `True`; el 9 devuelve `False`.

## Ejecución desde la raíz

```powershell
py -3.14 .\clean_code\07_useful_comments\before.py
py -3.14 .\clean_code\07_useful_comments\after.py
```

## Límite

Los comentarios también requieren mantenimiento. Si cambia la regla, actualiza
su explicación. Antes de añadir un comentario, evalúa si un nombre más claro
resolvería la confusión. El comentario inicial de cada archivo sirve como guía
de la lección; no intenta documentar cada instrucción.
