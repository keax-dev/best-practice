# Nombres de objetos de PostgreSQL

## ¿Qué es?

Es dar nombres consistentes a tablas, columnas y restricciones para reconocer su propósito.

## ¿Cómo funciona y para qué sirve?

La convención interna usa prefijos, mayúsculas y guiones bajos. PostgreSQL convierte los nombres sin comillas a minúsculas; las comillas dobles conservan las mayúsculas.

## Qué muestra el ejemplo

GEN es un prefijo ficticio. La tabla temporal permite probar nombres sin crear tablas permanentes.

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

Si se eligen identificadores entre comillas, habrá que mantenerlas en las consultas y en el mapeo ORM. El equipo debe acordar esa decisión. Los prefijos no son una exigencia del motor.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
