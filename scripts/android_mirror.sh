#!/bin/bash

# Enviar una notificación a Debian (si libnotify-bin está instalado)
if command -v notify-send &> /dev/null; then
    notify-send "Android Mirror" "Buscando dispositivo..." --icon=phone
else
    echo "Buscando dispositivo..."
fi

# Intentar localizar scrcpy (PATH o Snap)
SCRCPY_CMD="scrcpy"
if ! command -v scrcpy &> /dev/null; then
    if [ -f "/snap/bin/scrcpy" ]; then
        SCRCPY_CMD="/snap/bin/scrcpy"
    else
        echo "Error: scrcpy no encontrado. Asegúrate de instalarlo."
        if command -v notify-send &> /dev/null; then
            notify-send "Error" "scrcpy no encontrado." --urgency=critical
        fi
        exit 1
    fi
fi

# Esperar al dispositivo
# El timeout es opcional, pero evita que se quede colgado eternamente si no hay dispositivo
adb wait-for-device

if [ $? -eq 0 ]; then
    if command -v notify-send &> /dev/null; then
        notify-send "Android Mirror" "Dispositivo conectado. Iniciando..." --icon=phone
    else
        echo "Dispositivo conectado. Iniciando..."
    fi
    
    # Ejecutar scrcpy con optimizaciones para hardware antiguo
    # -m800: Max tamaño 800px
    # --max-fps=30: Limitar FPS
    # -b2M: Bitrate 2Mbps
    # -S: Apagar pantalla del móvil
    # --no-audio: No transmitir audio
    $SCRCPY_CMD -m800 --max-fps=30 -b2M -S --no-audio --window-title "Android Mirror"
else
    if command -v notify-send &> /dev/null; then
        notify-send "Error" "No se detectó el teléfono." --urgency=critical
    else
        echo "Error: No se detectó el teléfono."
    fi
fi
