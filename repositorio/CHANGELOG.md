# Cambios

## 0.1.0 — 2026-10-17

Primera versión preparada para compartir.

- Interfaz para ajustar entre 1 y 50 CPS, seleccionar una posición fija y contar clics enviados.
- Fuente predeterminada definida con `tkinter.font.Font` y etiquetas en Arial.
- Detección de F6 mediante consulta de estado de teclado en el hilo de trabajo.
- Esc como parada de emergencia, con prioridad sobre F6.
- Ejecutable de Windows sin consola, generado con PyInstaller.

### Validación realizada

- El usuario confirmó que la versión del código con F6 y Esc funcionó en su equipo.
- Comprobación de sintaxis y pruebas simuladas de F6, pulsación mantenida y prioridad de Esc.
- Compilación del ejecutable completada y cabecera verificada como aplicación de ventana sin consola.
- No se ha realizado una prueba visual del ejecutable generado ni una matriz de pruebas en otros equipos.
