# Columnas explícitas

## ¿Qué es?

Es indicar qué columnas necesitas leer o escribir en lugar de depender de toda la estructura de la tabla.

## ¿Cómo funciona y para qué sirve?

SELECT con nombres devuelve solo los campos necesarios. INSERT con columnas explícitas evita depender del orden físico.

## Qué muestra el ejemplo

La salida mejorada excluye email porque esta operación no lo necesita. Ambas versiones insertan los datos indicando las columnas.

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

No se afirma que SELECT * sea siempre incorrecto en todo contexto. Aquí se evita porque el contrato de consulta solo necesita dos campos.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
