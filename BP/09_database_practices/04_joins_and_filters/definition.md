# JOIN y filtros

## ¿Qué es?

Es relacionar tablas por sus claves y filtrar el resultado que realmente necesita la operación.

## ¿Cómo funciona y para qué sirve?

Un INNER JOIN expresa la relación entre pedido y cliente. Un filtro posterior limita los resultados sin producir combinaciones ajenas.

## Qué muestra el ejemplo

before.sql combina cada pedido con ambos clientes. after.sql relaciona cada pedido únicamente con su propietario.

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

CROSS JOIN es válido cuando sí necesitas un producto cartesiano. La práctica consiste en expresar la relación correcta. EXISTS y HAVING dependen de la pregunta de negocio.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
