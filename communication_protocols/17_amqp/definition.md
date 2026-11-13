# AMQP — Advanced Message Queuing Protocol

## ¿Qué es?

Un protocolo de mensajería para intercambiar mensajes entre aplicaciones.
Es habitual utilizarlo con un broker que recibe y distribuye el trabajo.

## ¿Cómo funciona y para qué sirve?

Un productor publica mensajes y uno o varios consumidores los procesan.
Las confirmaciones permiten comunicar recepción o procesamiento según la operación
y la configuración. Sirve para desacoplar servicios y distribuir tareas.

## Ideas clave

- **AMQP 0-9-1 y AMQP 1.0 son protocolos distintos**; cliente y broker deben coincidir.
- En RabbitMQ con 0-9-1, los exchanges enrutan mensajes hacia colas mediante bindings.
- Persistencia, confirmaciones y reentregas requieren configuración; puede haber duplicados.
- Los consumidores deben ser idempotentes cuando repetir una operación cause problemas.
- Puertos habituales: **5672** y **5671** con TLS.

**Referencia:** [Protocolos soportados por RabbitMQ](https://www.rabbitmq.com/docs/protocols).
