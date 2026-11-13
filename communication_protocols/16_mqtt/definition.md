# MQTT

## ¿Qué es?

Un protocolo de mensajería de publicación y suscripción, especialmente utilizado
en IoT y telemetría.

## ¿Cómo funciona y para qué sirve?

Los clientes se conectan a un **broker**. Un publicador envía un mensaje a un
tema, como `sensors/temperature`, y el broker lo distribuye a sus suscriptores.
Normalmente funciona sobre TCP, con TLS cuando se necesita proteger la conexión.

## Ideas clave

- QoS **0**: como máximo una entrega; **1**: al menos una; **2**: exactamente una
  dentro del intercambio de protocolo correspondiente.
- QoS no garantiza que un efecto de negocio se ejecute exactamente una vez de extremo a extremo.
- Los mensajes retenidos permiten entregar el último valor a nuevos suscriptores.
- Deben configurarse autenticación y permisos por tema.
- Puertos habituales: **1883** y **8883** con TLS.

**Referencia:** [MQTT 5.0, OASIS](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html).
