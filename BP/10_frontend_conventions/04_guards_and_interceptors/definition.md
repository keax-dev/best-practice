# Guards e interceptores

## ¿Qué es?

Un guard decide la navegación y un interceptor aplica comportamiento común a las solicitudes HTTP.

## ¿Cómo funciona y para qué sirve?

El guard consulta la sesión y redirige al login. El interceptor adjunta el token solo a la API permitida y excluye el login.

## Qué muestra el ejemplo

after.ts contiene funciones reales de Angular. Las pruebas comprueban redirección, token para la API y ausencia de token en dominios ajenos o rutas parecidas.

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

La sesión del ejemplo es simulada. El guard no verifica firmas JWT ni concede permisos de backend. El servidor siempre debe verificar token, rol y propiedad del recurso.

## Referencias

Consulta [angular](../../SOURCES.md#angular) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
