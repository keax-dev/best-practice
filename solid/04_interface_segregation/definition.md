# I: principio de segregación de interfaces

## ¿Qué es?

Es separar las operaciones en grupos para que cada clase implemente solo las
capacidades que realmente necesita ofrecer.

Una interfaz describe las operaciones que una clase debe tener. Si una interfaz
exige trabajar y comer, un robot tendrá que incluir una operación para comer
aunque no pueda realizarla. Separar ambas capacidades evita ese método inútil
y permite pedir a cada objeto únicamente lo que sabe hacer.

## Cuándo aporta

Cuando varias clases implementan métodos vacíos o lanzan errores porque una
interfaz reúne capacidades que no siempre van juntas.

## Qué muestra el ejemplo

`before.py` obliga a todos los `Worker` a trabajar y comer. `RobotWorker` puede
trabajar, pero implementa `eat` únicamente para lanzar `NotImplementedError`.
La demostración captura ese error y lo muestra como problema del diseño.

En `after.py`, `Workable` representa trabajar y `Eater` representa comer.
`HumanWorker` cumple ambos contratos; `RobotWorker` solo cumple `Workable`.
`run_shift` recibe trabajadores y `serve_lunch` recibe únicamente comensales.

La versión mejorada imprime el trabajo de la persona y del robot, y la comida
de la persona. No necesita preguntar si el objeto es un robot para evitar el fallo.

## Ejecución desde la raíz

```powershell
py -3.14 .\solid\04_interface_segregation\before.py
py -3.14 .\solid\04_interface_segregation\after.py
```

## Límite

No crees una interfaz por cada método sin considerar quién la consume. La
separación debe representar necesidades distintas, no solo fragmentar archivos.
En Python estos contratos también pueden expresarse con protocolos.
