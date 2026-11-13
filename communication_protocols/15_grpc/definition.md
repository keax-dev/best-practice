# gRPC

## ¿Qué es?

Una tecnología de llamadas a procedimientos remotos (**RPC**): permite invocar
operaciones de otro servicio mediante un contrato compartido.

## ¿Cómo funciona y para qué sirve?

Habitualmente se definen servicios y mensajes en archivos `.proto`. Las herramientas
generan modelos y código de comunicación para cliente y servidor. El desarrollador
implementa las operaciones. gRPC utiliza HTTP/2 y suele serializar con Protocol Buffers.

## Ideas clave

- Admite llamadas simples y transmisión de mensajes del cliente, servidor o ambos.
- Es útil entre servicios que necesitan contratos tipados y generación de código.
- Deben configurarse plazos de espera y seguridad; las llamadas pueden fallar.
- No es un protocolo de transporte como TCP o QUIC.
- En navegadores suele utilizarse gRPC-Web, con una integración o proxy compatible.

**Referencia:** [Conceptos fundamentales de gRPC](https://grpc.io/docs/what-is-grpc/core-concepts/).
