# Consultas parametrizadas

## ¿Qué es?

Es enviar los valores por separado del texto SQL para que no se interpreten como instrucciones.

## ¿Cómo funciona y para qué sirve?

PREPARE declara un parámetro $1. En Java se utiliza PreparedStatement o parámetros JPA; en Python el driver proporciona su mecanismo de parámetros.

## Qué muestra el ejemplo

La consulta anterior representa una condición alterada y devuelve ambos clientes. La parametrizada trata el mismo contenido como un nombre literal y no encuentra ninguno.

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

Los parámetros representan valores, no nombres de tabla o columnas. Para identificadores usa una lista permitida y las herramientas del driver. No construyas la consulta con f-strings.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
