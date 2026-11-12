# Estructura de un componente Angular

## ¿Qué es?

Es mantener juntos la clase, la plantilla y los estilos que pertenecen al mismo componente.

## ¿Cómo funciona y para qué sirve?

La clase expone datos y la plantilla decide cómo mostrarlos. El ejemplo utiliza un componente standalone y @for con una clave estable.

## Qué muestra el ejemplo

before.ts mezcla una plantilla extensa en la clase. after.ts referencia after.html y after.scss. Cada producto tiene id y name.

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

No se obliga a crear carpetas vacías para todas las categorías del manual. En un proyecto real se conservan su arquitectura y su estrategia de pruebas.

## Referencias

Consulta [angular](../../SOURCES.md#angular) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
