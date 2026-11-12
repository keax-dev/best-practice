# Restricciones y normalización

## ¿Qué es?

Es separar entidades y hacer que la base de datos proteja reglas esenciales, como claves y cantidades positivas.

## ¿Cómo funciona y para qué sirve?

La versión mejorada separa cliente y pedido, enlaza con una FK y aplica CHECK y NOT NULL. El bloque DO demuestra que la regla rechaza una cantidad negativa.

## Qué muestra el ejemplo

La versión anterior conserva una cantidad negativa. La posterior deja solo el pedido válido y comprueba que el motor rechaza el inválido.

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

Separar dos tablas no demuestra por sí solo toda la tercera forma normal. Analiza dependencias funcionales y requisitos antes de normalizar o desnormalizar.

## Referencias

Consulta [database](../../SOURCES.md#database) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
