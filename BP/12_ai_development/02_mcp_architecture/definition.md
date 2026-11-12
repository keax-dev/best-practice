# Arquitectura de un servidor MCP

## ¿Qué es?

Es separar las herramientas que expone un servidor MCP de la lógica y de las integraciones que utiliza.

## ¿Cómo funciona y para qué sirve?

Un adaptador MCP recibe la solicitud, un caso de uso trabaja contra puertos y los adaptadores conectan capacidades autorizadas. La guía interna pide usar servicios de soporte o gateways para recursos externos.

## Qué muestra el ejemplo

Compara el caso problemático de `before.md` con la respuesta propuesta en `after.md`.

Tecnología: **MCP y arquitectura**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

Lee los archivos de ejemplo indicados en esta carpeta. No levantan un servicio.

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Es un caso de diseño, no un servidor MCP listo para exponer. El término OAuth0 del manual necesita aclararse: no se adopta como nombre de un protocolo. La política interna no se presenta como una exigencia universal de MCP.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
