# Alternativas ante un fallo

## ¿Qué es?

Es ofrecer un resultado alternativo seguro cuando no puedes obtener el normal, dejando visible que hubo degradación.

## ¿Cómo funciona y para qué sirve?

Para una consulta de catálogo se puede devolver una copia previamente conocida e indicar que está desactualizada. No se inventa una confirmación de negocio.

## Qué muestra el ejemplo

La alternativa devuelve Coffee con stale=True. La política de usar ese dato debe estar acordada con negocio.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\04_fallbacks\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\04_fallbacks\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Un fallback de catálogo no autoriza confirmar pagos, saldos ni stock usando datos inventados. No deben encadenarse alternativas sin límites.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
