#!/bin/bash

# Detectar el directorio actual para configurar las rutas absolutas
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Instalador de Miru (v2.0) ==="
echo "Configurando en: $INSTALL_DIR"

# 1. Configurar miru-app.desktop con la ruta correcta
DESKTOP_FILE="miru-app.desktop"

echo "Actualizando rutas en $DESKTOP_FILE..."
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Miru
Comment=Android Development Suite
Exec=$INSTALL_DIR/start-app.sh
Icon=phone
Terminal=false
Categories=Development;Utility;
Keywords=android;adb;scrcpy;mirror;debug;
StartupNotify=true
EOF
chmod +x "$DESKTOP_FILE"

# 2. Dar permisos a los scripts
chmod +x scripts/*.sh
chmod +x start-app.sh
chmod +x miru-app.py

# 3. Limpiar accesos directos viejos (Legacy)
echo "Limpiando accesos directos antiguos..."
rm -f ~/.local/share/applications/android-*.desktop
if [ -d ~/Desktop ]; then rm -f ~/Desktop/android-*.desktop; fi
if [ -d ~/Escritorio ]; then rm -f ~/Escritorio/android-*.desktop; fi

# 4. Instalar nuevo acceso directo
mkdir -p ~/.local/share/applications
cp "$DESKTOP_FILE" ~/.local/share/applications/

# 5. Copiar al Escritorio
TARGET_DIR=""
if [ -d ~/Desktop ]; then TARGET_DIR=~/Desktop; fi
if [ -d ~/Escritorio ]; then TARGET_DIR=~/Escritorio; fi

if [ -n "$TARGET_DIR" ]; then
    cp "$DESKTOP_FILE" "$TARGET_DIR/"
    chmod +x "$TARGET_DIR/$DESKTOP_FILE"
    echo "✔ Acceso directo 'Miru' creado en el Escritorio"
fi

echo ""
echo "=== ¡Instalación Completada! ==="
echo "Ejecuta 'Miru' desde tu menú de aplicaciones o escritorio."
