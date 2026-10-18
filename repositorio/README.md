# Cookie AutoClicker 🍪

Autoclicker sencillo para Windows con interfaz gráfica, velocidad ajustable y parada por teclado.

Proyecto personal creado con ayuda de IA y probado por su autor. El código se comparte también como material de aprendizaje; su autor todavía está estudiando cómo funciona.

## Qué hace

- Clic izquierdo automático de 1 a 50 clics por segundo (CPS).
- Clic en la posición actual del cursor o en una posición fija.
- F6 para iniciar o detener; Esc para detener.
- Contador de clics enviados, con botón para reiniciarlo.
- Funcionamiento local: el código de la aplicación no usa red ni telemetría.

## Usar sin instalar Python

Si hay una versión publicada, abre la sección **Releases** de este repositorio, descarga `CookieAutoClicker.exe` y ejecútalo. El ejecutable abre únicamente la ventana de la aplicación.

1. Empieza a 1 CPS para probar los controles.
2. Coloca el cursor sobre el objetivo y pulsa **F6** para iniciar.
3. Pulsa **F6** otra vez o **Esc** para detener.
4. Para una posición fija, pulsa **Elegir posición**, mueve el cursor al objetivo y espera los tres segundos. Después inicia los clics.

En algunos teclados se necesita **Fn + F6**. Prueba las teclas antes de usar la posición fija. Si no puedes detenerlo, usa **Ctrl + Alt + Supr → Administrador de tareas** y finaliza CookieAutoClicker (o Python, si lo abriste desde el código).

## Ejecutar desde el código

Necesitas Windows y Python con Tkinter. La aplicación utiliza únicamente la biblioteca estándar; no necesitas instalar paquetes con pip para ejecutarla.

Haz doble clic en `INICIAR.bat` o, desde esta carpeta, ejecuta:

```bat
py cookie_autoclicker.py
```

Esta versión se ha usado en Windows con Python 3.14 y Tk 8.6. No se ha comprobado su compatibilidad con todas las versiones de Windows o Python.

## Crear el ejecutable

Haz doble clic en `CREAR_EXE.bat`. El script crea un entorno de compilación local, descarga PyInstaller y genera:

```text
dist/CookieAutoClicker.exe
```

Solo este paso necesita conexión para descargar las herramientas. No necesitas compilar si ya descargaste el ejecutable. `--windowed` evita la consola y `--onefile` reúne la aplicación en un archivo.

## Limitaciones

- Solo funciona en Windows y genera clics izquierdos.
- La velocidad es aproximada: depende del sistema y de la aplicación de destino.
- El contador registra clics enviados; no confirma que otra aplicación los haya recibido.
- F6 y Esc se consultan mientras la app está abierta, incluso cuando otra ventana tiene el foco. No se guarda un historial de teclas.
- En posición fija, la app mueve el cursor al punto seleccionado para cada clic.
- No se ha verificado el funcionamiento en pantallas de seguridad o aplicaciones con permisos elevados.
- El ejecutable compartido no tiene firma digital.

## Aprender y colaborar

Consulta [APRENDER.md](APRENDER.md) para recorrer el código y [CONTRIBUTING.md](CONTRIBUTING.md) para reportar errores o proponer cambios.

Los cambios de esta versión están en [CHANGELOG.md](CHANGELOG.md).

## Licencia

El código del proyecto se comparte bajo [licencia MIT](LICENSE), que permite usarlo, modificarlo y distribuirlo conservando el aviso de licencia. Las dependencias incluidas en el ejecutable conservan sus propias licencias.
