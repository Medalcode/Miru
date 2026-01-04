#!/bin/bash

# Detectar el directorio actual para configurar las rutas absolutas
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_PATH="phone" 

echo "=== Instalador Automático de Suite Android ==="
echo "Configurando en: $INSTALL_DIR"

# Función para generar desktop files dinámicamente
generate_desktop() {
    local NAME="$1"
    local SCRIPT="$2"
    local ICON="$3"
    local TERMINAL="$4"
    local FILE_NAME="$5"
    local COMMENT="$6"

    echo "Generando $NAME..."
    cat > "$FILE_NAME" <<EOF
[Desktop Entry]
Type=Application
Name=$NAME
Comment=$COMMENT
Exec=$INSTALL_DIR/scripts/$SCRIPT
Icon=$ICON
Terminal=$TERMINAL
Categories=Development;Utility;
StartupNotify=true
EOF
    chmod +x "$FILE_NAME"
}

# 1. Generar los archivos .desktop
# Mirror (Ver)
generate_desktop "Android Mirror" "android_mirror.sh" "phone" "false" "android-mirror.desktop" "Ver pantalla de mi Android antiguo"
# Record (Grabar)
generate_desktop "Android Record" "android_mirror.sh record" "media-record" "false" "android-record.desktop" "Grabar pantalla del Android"
# Snap (Foto)
generate_desktop "Android Snap" "android_screenshot.sh" "camera-photo" "false" "android-screenshot.desktop" "Captura de pantalla instantánea"
# HID (Teclado) - Nota: Usa el mismo script android_mirror.sh con argumento hid
generate_desktop "Android Type" "android_mirror.sh hid" "input-keyboard" "false" "android-hid.desktop" "Usar teclado físico PC en Android"
# Debug (Logs)
generate_desktop "Android Debug" "android_logcat.sh" "utilities-terminal" "true" "android-logcat.desktop" "Ver log de errores y crashes"
# Reset (Emergency)
generate_desktop "Android Reset" "android_reboot.sh" "system-reboot" "false" "android-reboot.desktop" "Reinicia móvil o arregla conexión ADB"


# 2. Dar permisos a los scripts
chmod +x scripts/*.sh

# 3. Instalar en el sistema
mkdir -p ~/.local/share/applications
cp android-*.desktop ~/.local/share/applications/

# 4. Copiar al Escritorio
TARGET_DIR=""
if [ -d ~/Desktop ]; then TARGET_DIR=~/Desktop; fi
if [ -d ~/Escritorio ]; then TARGET_DIR=~/Escritorio; fi

if [ -n "$TARGET_DIR" ]; then
    cp android-*.desktop "$TARGET_DIR/"
    chmod +x "$TARGET_DIR"/android-*.desktop
    echo "✔ Iconos creados en el Escritorio ($TARGET_DIR)"
fi

echo ""
echo "=== ¡Instalación Completada! ==="
echo "Suite de Herramientas Android - Total: 6"
echo "1. 📱 Android Mirror (Ver y Controlar)"
echo "2. 🔴 Android Record (Grabar Video)"
echo "3. 📸 Android Snap (Foto Instantánea)"
echo "4. ⌨️ Android Type (Teclado Físico)"
echo "5. 🐛 Android Debug (Ver Errores)"
echo "6. 🚑 Android Reset (Reiniciar/Arreglar)"
