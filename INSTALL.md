# Guía de Instalación y Configuración para Android Mirror

Sigue estos pasos para configurar tu sistema Debian y usar el script de mirroring optimizado.

## 1. Instalar Dependencias del Sistema

Abre una terminal y ejecuta los siguientes comandos para instalar `adb`, `scrcpy` y las utilidades de notificación:

```bash
sudo apt update
sudo apt install scrcpy adb libnotify-bin
```

## 2. Configurar el Acceso USB (Reglas udev/Permisos)

Para evitar problemas de permisos y no tener que usar `sudo` cada vez, añade tu usuario al grupo `plugdev`:

```bash
sudo usermod -aG plugdev $USER
```

_Nota: Es recomendable reiniciar la sesión o el equipo después de este cambio._

## 3. Instalar el Acceso Directo

Para que aparezca en tu menú de aplicaciones, copia el archivo `.desktop` a la carpeta de aplicaciones de tu usuario:

```bash
mkdir -p ~/.local/share/applications
cp android-mirror.desktop ~/.local/share/applications/
```

_Si decides mover la carpeta del proyecto, recuerda editar el archivo `.desktop` y actualizar la línea `Exec=` con la nueva ruta._

## 4. Crear un Alias (Opcional)

Si quieres ejecutarlo desde la terminal escribiendo solo `celular`, añade esto a tu `.bashrc`:

1.  Abre el archivo de configuración:
    ```bash
    nano ~/.bashrc
    ```
2.  Añade al final:
    ```bash
    alias celular='/home/medalcode/Antigravity/Miru/scripts/android_mirror.sh'
    ```
3.  Guarda (Ctrl+O) y sal (Ctrl+X).
4.  Recarga la configuración:
    ```bash
    source ~/.bashrc
    ```

## 5. Configurar Atajo de Teclado (Opcional)

### GNOME

1.  Ve a **Configuración** -> **Teclado** -> **Ver y personalizar atajos**.
2.  **Atajos personalizados** -> Añadir (+).
3.  Nombre: `Mirror Android`.
4.  Comando: `/home/medalcode/Antigravity/Miru/scripts/android_mirror.sh`.
5.  Asigna la tecla que prefieras (ej. `Ctrl + Alt + A`).

### XFCE

1.  **Configuración** -> **Teclado** -> **Atajos de aplicación**.
2.  Añadir -> Comando: `/home/medalcode/Antigravity/Miru/scripts/android_mirror.sh`.
3.  Asigna la tecla.

## Uso

1.  Conecta tu teléfono por USB.
2.  Asegúrate de tener la **Depuración USB** activada en el móvil.
3.  Ejecuta el programa (desde el menú, el alias o el atajo).
4.  La primera vez, mira la pantalla del móvil para **autorizar** la conexión ADB.

Si experimentas lag, el script ya está optimizado con:

- Resolución máx: 800px
- FPS máx: 30
- Bitrate: 2Mbps
- Pantalla móvil apagada (ahorro de energía y calor)
