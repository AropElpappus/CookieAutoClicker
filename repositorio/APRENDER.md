# Guía para estudiar el código

El programa está en `cookie_autoclicker.py`. Este recorrido permite estudiarlo por partes.

## 1. Ventana y estado

`AutoClicker` hereda de `tk.Tk`. Su constructor prepara la ventana, las variables de la interfaz y dos eventos de sincronización: `active` indica si deben generarse clics y `closed` indica que la aplicación debe terminar.

`_make_ui()` crea las etiquetas, botones y controles. La fuente predeterminada es un objeto `tkinter.font.Font` cuyo nombre se entrega a Tkinter. Así se evita interpretar incorrectamente una familia de fuente con espacios.

## 2. Iniciar y detener

`_toggle()` cambia entre activo y detenido. `_stop()` desactiva el evento de clics y actualiza la interfaz. La posición fija se captura con una cuenta regresiva programada mediante `after`, sin bloquear la ventana.

## 3. Trabajo en segundo plano

`_click_loop()` corre en un hilo separado. Usa funciones de Windows a través de `ctypes` para mover el cursor y enviar pulsaciones del botón izquierdo. `time.perf_counter()` sirve para calcular cuándo corresponde el próximo clic.

Ese hilo no modifica los controles de Tkinter: envía mensajes con una cola. `_poll()` los procesa en el hilo de la interfaz aproximadamente cada 30 milisegundos.

## 4. Teclado y parada

`_check_keys()` consulta el estado actual de F6 y Esc mediante `GetAsyncKeyState`. Guarda el estado anterior de F6 para actuar una vez por pulsación. Esc tiene prioridad y desactiva los clics desde el propio hilo de trabajo; la actualización visual llega después mediante la cola.

La espera entre clics se divide en intervalos cortos para seguir revisando las teclas incluso a 1 CPS. Esto no equivale a una garantía de respuesta inmediata en cualquier circunstancia.

## 5. Problemas que dieron origen a esta versión

- **Fuente mal interpretada:** una cadena como `Segoe UI 10` hizo que Tkinter intentara interpretar `UI` como tamaño. Cambiar una etiqueta no bastaba porque la opción global seguía usando esa cadena.
- **F6 sin respuesta:** la versión anterior combinaba `RegisterHotKey` con lectura manual de mensajes en el hilo de Tkinter. Se sustituyó por consulta del estado de las teclas y se añadió Esc.

## Ejercicios sugeridos

1. Cambia el título o los colores e identifica dónde se construye cada control.
2. Sigue el recorrido de un mensaje `click` desde el hilo hasta el contador.
3. Explica por qué mantener F6 pulsado no debería alternar repetidamente el estado.
4. Antes de cambiar el ritmo o los atajos, prueba a 1 CPS y sin posición fija.
