#!/bin/bash

# Directorio donde guardar las capturas (Escritorio es lo más cómodo)
SAVE_DIR="$HOME/Desktop"
if [ ! -d "$SAVE_DIR" ]; then
    SAVE_DIR="$HOME/Escritorio"
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
FILENAME="$SAVE_DIR/Android_Screenshot_$TIMESTAMP.png"

# Notificar inicio
if command -v notify-send &> /dev/null; then
    notify-send "Android Snap" "Tomando captura..." --icon=camera-photo
fi

# Comando mágico: adb exec-out screencap -p descarga la imagen directamente al pipe, sin guardarla en el móvil primero
# Se usa MIRU_ADB_DEVICE para evitar conflictos con múltiples dispositivos
adb $MIRU_ADB_DEVICE exec-out screencap -p > "$FILENAME"

if [ $? -eq 0 ]; then
    if command -v notify-send &> /dev/null; then
        notify-send "Captura Guardada" "En: $FILENAME" --icon=camera-photo
    fi
else
    if command -v notify-send &> /dev/null; then
        notify-send "Error" "No se pudo tomar la captura" --urgency=critical
    fi
fi
