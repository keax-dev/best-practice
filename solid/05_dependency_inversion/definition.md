# D: principio de inversión de dependencias

## ¿Qué es?

Es hacer que la lógica principal use una capacidad definida, sin quedar atada a
una herramienta específica que la realiza.

Por ejemplo, un servicio de pedidos necesita enviar una notificación. Puede pedir
un objeto que tenga la operación `send`, sin decidir dentro del servicio si será
correo o SMS. Un contrato describe esa operación y, desde fuera, se proporciona
la implementación elegida. Así puedes cambiar el canal sin reescribir la
confirmación del pedido.

## Cuándo aporta

Cuando necesitas cambiar un proveedor externo, un repositorio o un canal de
notificación, o sustituirlo por un doble durante las pruebas.

## Qué muestra el ejemplo

En `before.py`, `OrderService` construye `EmailSender`. Cambiar a otro canal
requiere editar el propio servicio.

En `after.py`, el servicio recibe un `MessageSender` por el constructor.
El protocolo describe `send(message)` y tanto `EmailSender` como `SmsSender`
ofrecen ese método sin heredar explícitamente del protocolo.

`main` elige las implementaciones. La versión anterior envía un correo simulado;
la posterior demuestra correo y SMS simulados. No se realizan llamadas externas.

## Inversión frente a inyección

Inyectar significa proporcionar una dependencia desde fuera. Invertir las
dependencias significa orientar el diseño hacia un contrato. Pasar una clase
concreta por un constructor no aplica automáticamente todo el principio.

## Ejecución desde la raíz

```powershell
py -3.14 .\solid\05_dependency_inversion\before.py
py -3.14 .\solid\05_dependency_inversion\after.py
```

## Límite

`Protocol` sirve para el tipado estructural; aquí no valida implementaciones en
tiempo de ejecución. Tampoco necesitas un contenedor de inyección: el constructor
y la composición explícita bastan para este ejemplo.

Referencia: [Protocol en Python](https://docs.python.org/3.14/library/typing.html#typing.Protocol).
