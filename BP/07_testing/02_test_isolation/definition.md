# Aislamiento entre pruebas

## ¿Qué es?

Es evitar que el resultado de una prueba dependa de lo que dejó otra.

## ¿Cómo funciona y para qué sirve?

Crea repositorios nuevos para cada caso. El fixture de esta carpeta carga un módulo independiente en cada prueba y el objeto devuelve copias de su colección.

## Qué muestra el ejemplo

El segundo repositorio empieza vacío. La prueba comprueba también que modificar una lista devuelta no altere el almacenamiento.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\02_test_isolation\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\02_test_isolation\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
