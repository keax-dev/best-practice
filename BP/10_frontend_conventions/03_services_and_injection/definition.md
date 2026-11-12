# Servicios e inyección en Angular

## ¿Qué es?

Es poner una operación reutilizable en un servicio y dejar que Angular lo entregue al componente.

## ¿Cómo funciona y para qué sirve?

inject obtiene una dependencia declarada. La vista presenta datos sin tener que construir el servicio ni conocer toda su lógica.

## Qué muestra el ejemplo

before.ts calcula directamente en el componente. after.ts recibe PricingService y delega el cálculo. La prueba usa el inyector de Angular.

Tecnología: **Angular**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
cd .\BP\10_frontend_conventions
npm ci
npm test
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Un servicio no necesita existir para envolver cada expresión simple. Aquí la separación muestra una regla que podría compartirse entre pantallas.

## Referencias

Consulta [angular](../../SOURCES.md#angular) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
