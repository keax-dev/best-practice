# Clean Code

## ¿Qué es Clean Code?

Es escribir código que puedas leer y entender con facilidad, incluso después
de un tiempo o cuando lo escribió otra persona.

Para conseguirlo, se usan nombres claros, funciones con tareas concretas y
errores fáciles de identificar. Por ejemplo, `calculate_order_total` explica
mejor una operación que `calc`. No hay una única forma correcta de escribir todo:
las prácticas deben ayudar a entender el programa, no complicarlo.

| Orden | Práctica | Teoría y ejemplo |
|---|---|---|
| 1 | Nombres claros | [Definición](01_clear_naming/definition.md) |
| 2 | Funciones pequeñas y coherentes | [Definición](02_small_functions/definition.md) |
| 3 | Evitar duplicación de reglas | [Definición](03_avoid_duplication/definition.md) |
| 4 | Salidas tempranas | [Definición](04_guard_clauses/definition.md) |
| 5 | Constantes con significado | [Definición](05_replace_magic_numbers/definition.md) |
| 6 | Manejo explícito de errores | [Definición](06_explicit_error_handling/definition.md) |
| 7 | Comentarios útiles | [Definición](07_useful_comments/definition.md) |

Cada carpeta tiene `definition.md`, `before.py` y `after.py`. Los archivos son
independientes. Desde la raíz puedes ejecutar, por ejemplo:

```powershell
py -3.14 .\clean_code\04_guard_clauses\before.py
py -3.14 .\clean_code\04_guard_clauses\after.py
```

Los ejemplos conservan el comportamiento al mejorar la expresión del código,
salvo el manejo de errores, donde se muestra explícitamente el cambio de ocultar
un fallo a comunicarlo. No se establece un límite universal de líneas para las
funciones ni se extraen constantes para todos los números.

Referencia de estilo específica de Python: [PEP 8](https://peps.python.org/pep-0008/).
