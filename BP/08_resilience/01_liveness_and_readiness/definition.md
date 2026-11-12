# Liveness y readiness

## ¿Qué es?

Son dos preguntas distintas: ¿el proceso puede seguir funcionando? y ¿puede recibir tráfico ahora?

## ¿Cómo funciona y para qué sirve?

Liveness comprueba el proceso; readiness considera si están listas las condiciones críticas para atender. Una dependencia caída no debería convertir automáticamente el proceso en muerto.

## Qué muestra el ejemplo

La dependencia no disponible deja Live: True y ready: False. La aplicación Spring Boot expone grupos de salud con Actuator.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\01_liveness_and_readiness\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\01_liveness_and_readiness\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Un endpoint que devuelve OK no detecta todos los bloqueos ni las fugas de memoria. Los probes y sus umbrales requieren diseño y configuración de la plataforma.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
