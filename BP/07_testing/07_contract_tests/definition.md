# Pruebas de contrato

## ¿Qué es?

Es comprobar que lo que se envía o recibe respeta un acuerdo de campos, tipos y restricciones.

## ¿Cómo funciona y para qué sirve?

El ejemplo usa JSON Schema como contrato de un cuerpo JSON. La prueba verifica ejemplos válidos e inválidos contra ese archivo, sin duplicar sus reglas en otra función.

## Qué muestra el ejemplo

contract.json describe quantity entero positivo y no permite campos extra. example.py carga ese contrato y valida el mensaje.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\07_testing\07_contract_tests\example.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Un esquema JSON no describe por sí solo toda una API OpenAPI: faltan rutas, métodos y códigos HTTP. Esta carpeta enseña la validación del mensaje, no un proveedor OpenAPI completo.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
