# Funciones y métodos

## ¿Qué es?

Es reconocer qué operaciones necesitan un objeto, cuáles necesitan su clase y cuáles pueden ser funciones independientes.

## ¿Cómo funciona y para qué sirve?

Los métodos de instancia reciben self. Los métodos de clase reciben cls y pueden ofrecer constructores alternativos. Para una función con nombre, usa def en lugar de asignar una lambda.

## Qué muestra el ejemplo

Ambas versiones imprimen 10. El constructor alternativo es solo una demostración de cls; para crear este objeto también basta Order(5, 2).

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\05_functions_and_methods\before.py
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\05_functions_and_methods\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

No conviertas todas las funciones en clases. Una lambda breve como argumento de sorted sigue siendo apropiada cuando mejora la lectura.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
