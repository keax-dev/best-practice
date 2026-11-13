# Protocolos de comunicación

Un protocolo es un conjunto de reglas para intercambiar información: define el
formato de los mensajes, cómo se envían y cómo se interpretan las respuestas.
Aquí encontrarás teoría breve, sin código ni instalaciones.

## Ideas necesarias

- **Cliente y servidor:** uno inicia una solicitud y el otro ofrece un servicio.
- **Dirección IP:** identifica una interfaz de red; el **puerto** distingue servicios
  dentro de un equipo. Un nombre DNS facilita encontrar direcciones.
- **Paquete:** unidad de información que viaja por una red. Cada capa añade datos
  de control; este proceso se llama **encapsulación**.
- **Latencia:** tiempo de espera; **ancho de banda:** capacidad del enlace;
  **jitter:** variación de la latencia; **pérdida:** datos que no llegan.
- **Síncrono/asíncrono:** describe cómo una aplicación espera o procesa resultados.
  Usar HTTP no obliga a ejecutar todo el trabajo de forma síncrona.

## Capas y orden de lectura

OSI organiza la comunicación en siete capas: física, enlace, red, transporte,
sesión, presentación y aplicación. El modelo TCP/IP suele agruparlas en acceso
a red, internet, transporte y aplicación. Son modelos para entender responsabilidades;
no todos los protocolos encajan de manera exacta en una sola capa.

| Grupo | Lecturas |
|---|---|
| Acceso a la red | [Ethernet](01_ethernet/definition.md), [Wi-Fi](02_wifi/definition.md), [ARP](03_arp/definition.md) |
| Red | [IP](04_ip/definition.md), [ICMP](05_icmp/definition.md) |
| Nombres | [DNS](06_dns/definition.md) |
| Transporte | [TCP](07_tcp/definition.md), [UDP](08_udp/definition.md), [QUIC](13_quic/definition.md) |
| Seguridad | [TLS](09_tls/definition.md), [DTLS](10_dtls/definition.md) |
| Web y APIs | [HTTP](11_http/definition.md), [HTTPS](12_https/definition.md), [WebSocket](14_websocket/definition.md), [gRPC](15_grpc/definition.md) |
| Mensajería e IoT | [MQTT](16_mqtt/definition.md), [AMQP](17_amqp/definition.md), [CoAP](18_coap/definition.md) |
| Archivos | [FTP](19_ftp/definition.md), [SFTP](20_sftp/definition.md) |
| Correo | [SMTP](21_smtp/definition.md), [IMAP](22_imap/definition.md), [POP3](23_pop3/definition.md) |

Para tu ejercicio de Angular y microservicios, prioriza **DNS → TCP/UDP → TLS →
HTTP/HTTPS → WebSocket → gRPC → MQTT/AMQP**. Las demás carpetas amplían el contexto.

## Cómo trabajan juntos

Al consultar una API, DNS puede resolver su nombre. Con HTTP/1.1 o HTTP/2 sobre
HTTPS, el cliente establece TCP y TLS y después intercambia mensajes HTTP.
HTTP/3 utiliza QUIC sobre UDP, con seguridad integrada mediante TLS 1.3.
IP transporta los paquetes y Ethernet o Wi-Fi los llevan por el enlace local.

## Cómo elegir

| Necesidad | Opción habitual |
|---|---|
| APIs para Angular y otros clientes | HTTPS; REST puede orientar el diseño de los recursos |
| Actualizaciones bidireccionales continuas | WebSocket seguro (`wss`) |
| Llamadas entre servicios con contratos tipados | gRPC |
| Telemetría y publicación por temas | MQTT |
| Mensajería entre aplicaciones con confirmaciones | AMQP y un broker compatible |
| Dispositivos con recursos limitados | CoAP, según la red y sus requisitos |

**REST es un estilo arquitectónico**, no un protocolo. **gRPC es una tecnología
de RPC** que define cómo invocar operaciones remotas. Un broker es un intermediario
de mensajes; RabbitMQ es un producto que soporta varios protocolos.

Los puertos mencionados en las fichas son habituales, no obligatorios. Cifrar
una conexión no sustituye la autenticación ni los permisos del usuario. Tampoco
el transporte garantiza que una operación de negocio se ejecute una sola vez:
hay que contemplar timeouts, reintentos e idempotencia.

## Referencias

El [material de referencia de Technik](https://technik.es/protocolos-de-comunicacion/)
sirve como panorama inicial. Cada ficha enlaza una especificación o documentación
oficial para ampliar el tema. Los protocolos de enrutamiento, PPP y tecnologías
móviles quedan fuera de este resumen orientado al desarrollo de aplicaciones.
