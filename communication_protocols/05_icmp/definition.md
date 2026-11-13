# ICMP — Internet Control Message Protocol

## ¿Qué es?

Un protocolo de control que comunica diagnósticos y problemas relacionados con
la entrega de paquetes IP. ICMPv4 e ICMPv6 corresponden a IPv4 e IPv6.

## ¿Cómo funciona y para qué sirve?

Envía mensajes como destino inaccesible, tiempo excedido o solicitud/respuesta
de eco. `ping` utiliza mensajes de eco; `traceroute` aprovecha respuestas de
tiempo excedido para descubrir saltos de red.

## Ideas clave

- No usa puertos TCP ni UDP.
- Un `ping` exitoso no demuestra que una API o una base de datos funcionen.
- Una ausencia de respuesta puede deberse a filtros, no necesariamente a una caída.
- ICMPv6 también cumple funciones esenciales para el funcionamiento de IPv6.

**Referencia:** [ICMPv6: RFC 4443](https://www.rfc-editor.org/rfc/rfc4443.html).
