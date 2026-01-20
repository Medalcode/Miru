#!/bin/bash

# Carpeta para guardar grabaciones
REC_DIR="$HOME/Videos/Android_Recordings"
mkdir -p "$REC_DIR"

# Notificación inicial
if command -v notify-send &> /dev/null; then
    notify-send "Android Hub" "Buscando dispositivo..." --icon=phone
else
    echo "Buscando dispositivo..."
fi

# Detectar binario scrcpy
SCRCPY_CMD="scrcpy"
if ! command -v scrcpy &> /dev/null; then
    if [ -f "/snap/bin/scrcpy" ]; then
        SCRCPY_CMD="/snap/bin/scrcpy"
    fi
fi

# Esperar conexión usando el selector específico
adb $MIRU_ADB_DEVICE wait-for-device

if [ $? -eq 0 ]; then
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
    
    # Argumentos Base
    BASE_ARGS="-m1024 --max-fps=30 -b4M -S --no-audio --window-title"

    # Selector de Modos
    case "$1" in
        "record")
            FILENAME="$REC_DIR/Demo_$TIMESTAMP.mp4"
            # --show-touches: Vital para ver qué tocas en el video
            ARGS="$BASE_ARGS 'Android REC' --record $FILENAME --show-touches"
            MSG="🔴 Grabando: $FILENAME"
            TITLE="Android Rec"
            ;;
        "hid")
            # -K: Activa teclado HID (USB físico simulado)
            # --otg: SOLO teclado/ratón (sin video), pero aquí preferimos ver video + teclado físico
            # Usaremos -K junto con el video normal para la mejor experiencia
            ARGS="$BASE_ARGS 'Android Keyboard' -K"
            MSG="⌨️ Modo Teclado Físico Activo (Escribe directo)"
            TITLE="Android Type"
            ;;
        *)
            # Modo Estándar
            ARGS="$BASE_ARGS 'Android Mirror' --show-touches"
            MSG="🟢 Conectado"
            TITLE="Android Mirror"
            ;;
    esac

    if command -v notify-send &> /dev/null; then
        notify-send "$TITLE" "$MSG" --icon=input-keyboard
    fi
    
    # Ejecutar (eval para procesar correctamente las comillas en window-title)
    eval $SCRCPY_CMD $ARGS
else
    if command -v notify-send &> /dev/null; then
        notify-send "Error" "No se detectó el teléfono." --urgency=critical
    fi
fi
