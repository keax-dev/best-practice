# Nombres en Angular

## ¿Qué es?

Es reconocer el propósito de un componente por su clase y su selector.

## ¿Cómo funciona y para qué sirve?

Los ejemplos siguen la convención interna: clases PascalCase con sufijo Component y selectores con prefijo y guiones.

## Qué muestra el ejemplo

before.ts usa nombres ambiguos. after.ts define ProductListComponent con selector demo-product-list. El compilador verifica ambas plantillas.

Tecnología: **Angular y TypeScript**.

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

Los sufijos son una convención corporativa que puede diferir de otras guías o generaciones de Angular. Las variantes funcionales de guards e interceptores tienen tratamiento distinto en el manual.

## Referencias

Consulta [angular](../../SOURCES.md#angular) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
