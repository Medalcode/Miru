#!/bin/bash

# Carpeta para guardar las grabaciones de las demos
REC_DIR="$HOME/Videos/Android_Recordings"
mkdir -p "$REC_DIR"

# Enviar una notificación a Debian
if command -v notify-send &> /dev/null; then
    notify-send "Android Mirror" "Buscando dispositivo..." --icon=phone
else
    echo "Buscando dispositivo..."
fi

# Detectar scrcpy
SCRCPY_CMD="scrcpy"
if ! command -v scrcpy &> /dev/null; then
    if [ -f "/snap/bin/scrcpy" ]; then
        SCRCPY_CMD="/snap/bin/scrcpy"
    fi
fi

# Esperar al dispositivo
adb wait-for-device

if [ $? -eq 0 ]; then
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
    
    # Argumentos Base para Dev (Optimizados pero funcionales)
    # -m1024: Subimos un poco la calidad para leer texto (código)
    # -b4M: Más ancho de banda para mejor definición
    # --show-touches: Círculo blanco al tocar (Vital para demos)
    # --stay-awake: Evita que el móvil se duerma mientras trabajas
    ARGS="-m1024 --max-fps=30 -b4M -S --no-audio --show-touches --stay-awake --window-title 'Android DevTools'"

    # Lógica de Grabación
    if [ "$1" == "record" ]; then
        FILENAME="$REC_DIR/Demo_$TIMESTAMP.mp4"
        ARGS="$ARGS --record $FILENAME"
        MSG="🔴 Grabando sesión en: $FILENAME"
        TITLE="Android Rec"
    else
        MSG="🟢 Conectado (Portapapeles + APK Drag&Drop activos)"
        TITLE="Android Mirror"
    fi

    if command -v notify-send &> /dev/null; then
        notify-send "$TITLE" "$MSG" --icon=video-display
    fi
    
    # Ejecutar
    $SCRCPY_CMD $ARGS
else
    if command -v notify-send &> /dev/null; then
        notify-send "Error" "No se detectó el teléfono." --urgency=critical
    fi
fi
