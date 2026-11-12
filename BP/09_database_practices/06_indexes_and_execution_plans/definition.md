# Índices y planes de ejecución

## ¿Qué es?

Es medir cómo el motor encuentra filas y decidir si un índice ayuda a una consulta concreta.

## ¿Cómo funciona y para qué sirve?

EXPLAIN muestra el plan estimado. La versión mejorada agrega un índice por customer_id y actualiza estadísticas antes de consultar.

## Qué muestra el ejemplo

Ambas devuelven diez pedidos. El verificador confirma el resultado, pero no exige que el planificador elija siempre un tipo de acceso.

Tecnología: **SQL de PostgreSQL**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
cd .\BP\09_database_practices
npm ci
npm test
```

## Qué pide la organización

Se conserva la intención de los manuales de base de datos. La sintaxis se adapta a PostgreSQL; no se trasladan BIT, sp_executesql ni collations de SQL Server.

## Límites y aclaraciones

Crear índices tiene coste en escrituras y espacio. No hay una regla universal de particionar a partir de 2 GB. El entorno embebido sirve para aprender, no para certificar rendimiento productivo.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
