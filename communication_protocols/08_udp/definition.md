# UDP — User Datagram Protocol

## ¿Qué es?

Un protocolo de transporte que envía mensajes independientes llamados datagramas,
sin establecer previamente una conexión.

## ¿Cómo funciona y para qué sirve?

Cada envío conserva su límite de mensaje. UDP no incorpora confirmaciones,
retransmisión ni ordenación. Se utiliza en DNS, comunicaciones multimedia y como
base de otros protocolos, como QUIC.

## Ideas clave

- Los datagramas pueden perderse, duplicarse o llegar desordenados.
- La aplicación o un protocolo superior decide cómo tratar esas situaciones.
- Su menor sobrecarga no significa que siempre sea más rápido que TCP.
- No cifra datos. Protocolos superiores pueden añadir seguridad y fiabilidad.
- Conviene evitar mensajes que requieran fragmentación IP.

**Referencia:** [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html).
