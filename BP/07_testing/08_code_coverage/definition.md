# Cobertura de código

## ¿Qué es?

Es medir qué instrucciones y ramas se ejecutaron durante las pruebas. No mide si las comprobaciones son correctas.

## ¿Cómo funciona y para qué sirve?

pytest-cov genera un reporte. La lección usa una decisión con dos caminos para mostrar por qué hace falta probar cantidades válidas e inválidas.

## Qué muestra el ejemplo

Ejecuta pytest con --cov=BP/07_testing/08_code_coverage --cov-branch --cov-config=BP/.coveragerc para medir esta carpeta.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\08_code_coverage\before.py
.\.venv\Scripts\python.exe -B .\BP\07_testing\08_code_coverage\after.py
```

## Qué pide la organización

Las guías mencionan 75 % con alcances diferentes; el estándar de mutación menciona además cobertura unitaria >75 %. Se debe aclarar la métrica exigida antes de configurar el pipeline.

## Límites y aclaraciones

Un 100 % de cobertura puede coexistir con pruebas que no verifican resultados. El umbral es una política del equipo, no una medida universal de calidad.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
