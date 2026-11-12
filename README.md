# Buenas prácticas de desarrollo con Python

## ¿Qué son las buenas prácticas de desarrollo?

Son formas de escribir y organizar código para que sea más fácil entenderlo,
cambiarlo y detectar errores. Por ejemplo, dar un nombre claro a una función
ayuda a saber qué hace; separar el cálculo de una factura de su presentación
permite cambiar el formato sin tocar el cálculo.

Este repositorio enseña esas ideas con ejemplos independientes de **SOLID** y
**Clean Code**. Cada práctica tiene su explicación en `definition.md`, un código
que muestra el problema en `before.py` y una versión mejorada en `after.py`.

También incluye [BP: prácticas aplicadas al trabajo](BP/README.md), organizadas
en 12 bloques y adaptadas a Python, Spring Boot, Angular y PostgreSQL. Ese material
añade configuración, logging, pruebas, recursos, resiliencia y procesos de entrega.
Su guía explica las dependencias y comandos específicos de cada tecnología.

Los comentarios y la documentación están en español. Los identificadores, nombres
de archivo y mensajes del programa están en inglés. Los ejemplos de SOLID y Clean
Code utilizan solo la biblioteca estándar y están pensados para Python **3.14.7**.

## Preparación

Abre PowerShell en la carpeta del repositorio y verifica Python:

```powershell
cd C:\Users\jimen\Documents\coe-ing
py -3.14 --version
```

El entorno verificado es Python 3.14.7. Para SOLID y Clean Code no necesitas
instalar paquetes, crear una base de datos ni levantar un servidor. Tampoco
necesitas un entorno virtual para esos archivos. Para BP sigue su propia guía.

## Cómo estudiar y ejecutar un ejemplo

1. Lee el `definition.md` del principio.
2. Revisa y ejecuta `before.py` para identificar el problema.
3. Revisa y ejecuta `after.py` para comprender la alternativa.
4. Compara el diseño y los resultados de ambas versiones.

Por ejemplo, desde la raíz del repositorio:

```powershell
py -3.14 .\solid\01_single_responsibility\before.py
py -3.14 .\solid\01_single_responsibility\after.py
```

Ambos imprimen `Invoice total: 100 credits`. Lo que cambia es cómo se distribuyen
las responsabilidades, no el importe.

También puedes abrir una carpeta y ejecutar `py -3.14 before.py` y
`py -3.14 after.py` desde ella. Ningún archivo importa otro ejemplo.

## Contenido y orden sugerido

Primero estudia [Clean Code](clean_code/README.md), que trabaja la lectura de
funciones y las decisiones cotidianas al escribir código. Después continúa con
[SOLID](solid/README.md), que se concentra en contratos, clases y dependencias.

```text
clean_code/
    README.md
    01_clear_naming/
    02_small_functions/
    03_avoid_duplication/
    04_guard_clauses/
    05_replace_magic_numbers/
    06_explicit_error_handling/
    07_useful_comments/
solid/
    README.md
    01_single_responsibility/
    02_open_closed/
    03_liskov_substitution/
    04_interface_segregation/
    05_dependency_inversion/
```

Cada carpeta numerada contiene exactamente `before.py`, `after.py` y
`definition.md`. Los directorios numerados organizan las lecciones, no son paquetes
Python. Por eso no requieren archivos `__init__.py`.

## Qué significa la comparación

`before.py` es un contraejemplo intencional. Se puede ejecutar, pero muestra una
dificultad concreta de lectura, extensión o comportamiento. `after.py` ilustra una
mejora para ese caso, no una receta obligatoria para cualquier programa.

En nombres, funciones pequeñas, duplicación, salidas tempranas, constantes,
comentarios, responsabilidad única y abierto/cerrado, ambas versiones conservan
la salida de la demostración. En Liskov e interfaces, la versión anterior exhibe
el contrato roto. En inversión de dependencias, la posterior añade un canal de
notificación. En manejo de errores, la posterior comunica el fallo en lugar de
ocultarlo. Estas diferencias se explican en sus definiciones.

Las cantidades en `credits` son enteros ficticios para centrarse en el diseño.
Los type hints documentan contratos y ayudan a los analizadores estáticos, pero
no validan datos en tiempo de ejecución por sí solos. Los ejemplos no pretenden
resolver toda validación de negocio ni construir una aplicación de producción.

## Ejecutar todas las demostraciones

Desde la raíz, este comando ejecuta ambos archivos de las doce lecciones y se
detiene si alguno falla:

```powershell
Get-ChildItem -Path .\clean_code, .\solid -Recurse -Filter *.py |
    Sort-Object FullName |
    ForEach-Object {
        Write-Host "Running $($_.FullName)"
        py -3.14 -B $_.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "Example failed: $($_.FullName)"
        }
    }
```

La opción `-B` evita escribir archivos `.pyc`. Ejecutar todas las demostraciones
confirma que los archivos arrancan, pero no sustituye pruebas de comportamiento.
Para estudiar un principio, sigue el orden `before.py` y después `after.py`.

## Referencias

- [PEP 8: convenciones de estilo de Python](https://peps.python.org/pep-0008/).
- [Robert C. Martin: relevancia de SOLID](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html).
- [Python: clases base abstractas](https://docs.python.org/3.14/library/abc.html).
- [Python: protocolos y tipado estructural](https://docs.python.org/3.14/library/typing.html#typing.Protocol).
- [Python: errores y excepciones](https://docs.python.org/3.14/tutorial/errors.html).

Las definiciones son explicaciones originales acompañadas de ejemplos de este
repositorio. Las referencias amplían los conceptos y los mecanismos de Python.
