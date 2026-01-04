#!/bin/bash

# Detectar el directorio actual para configurar las rutas absolutas
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$INSTALL_DIR/scripts/android_mirror.sh"
ICON_PATH="phone" # Usamos un icono genérico del sistema, o podríamos usar una ruta a un png local

echo "=== Instalador Automático de Android Mirror ==="
echo "Configurando en: $INSTALL_DIR"

# 1. Crear el archivo .desktop con la ruta dinámica correcta
echo "Generando lanzador..."
cat > android-mirror.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Android Mirror
Comment=Ver pantalla de mi Android antiguo
Exec=$SCRIPT_PATH
Icon=$ICON_PATH
Terminal=false
Categories=Development;Utility;
StartupNotify=true
EOF

# 2. Dar permisos de ejecución
chmod +x android-mirror.desktop
chmod +x scripts/android_mirror.sh

# 3. Instalar en el sistema (Menú de aplicaciones)
mkdir -p ~/.local/share/applications
cp android-mirror.desktop ~/.local/share/applications/

# 4. Copiar al Escritorio (si existe) para tener el "doble click" ahí mismo
if [ -d ~/Desktop ]; then
    cp android-mirror.desktop ~/Desktop/
    chmod +x ~/Desktop/android-mirror.desktop
    echo "✔ Icono creado en el Escritorio"
fi

if [ -d ~/Escritorio ]; then
    cp android-mirror.desktop ~/Escritorio/
    chmod +x ~/Escritorio/android-mirror.desktop
    echo "✔ Icono creado en el Escritorio"
fi

echo ""
echo "=== ¡Instalación Completada! ==="
echo "Ahora puedes:"
echo "1. Buscar 'Android Mirror' en tu menú de inicio."
echo "2. O hacer doble clic en el icono de tu escritorio."
echo ""
echo "NOTA: Si es la primera vez, asegúrate de tener instalado 'adb' y 'scrcpy'."
echo "Comando rápido de instalación: sudo apt update && sudo apt install scrcpy adb libnotify-bin"
