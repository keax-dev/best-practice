# SOLID

## ¿Qué es SOLID?

Es un grupo de cinco principios que ayuda a organizar clases para que sea más
fácil cambiar una parte del programa sin romper otras. Cada letra propone una
idea: separar tareas, permitir nuevas opciones, respetar lo que promete una
clase, dividir capacidades y evitar depender de una herramienta específica.

Por ejemplo, puedes cambiar el envío de una notificación de correo a SMS sin
reescribir la lógica que confirma un pedido. Los ejemplos muestran cómo lograrlo
y cuándo no vale la pena agregar más clases.

| Orden | Principio | Teoría y ejemplo |
|---|---|---|
| 1 | S: responsabilidad única | [Definición](01_single_responsibility/definition.md) |
| 2 | O: abierto/cerrado | [Definición](02_open_closed/definition.md) |
| 3 | L: sustitución de Liskov | [Definición](03_liskov_substitution/definition.md) |
| 4 | I: segregación de interfaces | [Definición](04_interface_segregation/definition.md) |
| 5 | D: inversión de dependencias | [Definición](05_dependency_inversion/definition.md) |

Lee la definición y luego compara los dos archivos de su carpeta. Todos se
ejecutan por separado y sin dependencias externas. Por ejemplo, desde la raíz:

```powershell
py -3.14 .\solid\02_open_closed\before.py
py -3.14 .\solid\02_open_closed\after.py
```

En Python podemos expresar contratos con clases abstractas, protocolos o acuerdos
de comportamiento. Heredar de una clase no garantiza por sí mismo que se respete
su contrato. Los ejemplos usan `ABC` y `Protocol` para hacer visibles estas ideas.

**Criterio de aplicación:** introduce una separación cuando exista una razón
concreta de cambio, sustitución o mantenimiento. Un condicional breve puede ser
más apropiado que una jerarquía si no necesitas extensión independiente.

Referencia conceptual: [SOLID Relevance, Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html).
