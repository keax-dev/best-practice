# Importaciones claras

## ¿Qué es?

Es mostrar explícitamente de dónde viene cada herramienta que utiliza un archivo.

## ¿Cómo funciona y para qué sirve?

Separa imports de módulos y evita importar todo con asterisco. Así puedes identificar el origen de un nombre y reducir colisiones.

## Qué muestra el ejemplo

Ambos calculan la raíz entera de 81. La versión mejorada importa únicamente isqrt.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\02_imports\before.py
.\.venv\Scripts\python.exe -B .\BP\01_python_standards\02_imports\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
