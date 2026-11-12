# Nombres y estilo

## ¿Qué es?

Es elegir nombres que permitan saber qué representa cada dato y mantener el mismo estilo en todo el archivo.

## ¿Cómo funciona y para qué sirve?

Usa snake_case para funciones y variables, CapWords para clases y MAYÚSCULAS para constantes. En Python la indentación del ejemplo utiliza cuatro espacios.

## Qué muestra el ejemplo

Ambas versiones imprimen 10. La diferencia es si puedes entender la función sin descifrar abreviaturas. Amplía la explicación en [nombres claros](../../../clean_code/01_clear_naming/definition.md).

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\01_naming_and_style\before.py
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\01_naming_and_style\after.py
```

## Qué pide la organización

El manual Python pide inglés, cuatro espacios y líneas de hasta 120 caracteres. Ese límite es una convención interna, no una regla única para todos los proyectos.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
