#!/bin/bash

# Miru Native Application Launcher
# Inicia la aplicación nativa de Linux con GTK

echo "🚀 Iniciando Miru (Aplicación Nativa)..."
echo "========================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    exit 1
fi

# Verificar ADB
if ! command -v adb &> /dev/null; then
    echo "⚠️  Advertencia: ADB no está instalado"
    echo "   Instala con: sudo apt install adb"
fi

# Verificar scrcpy
if ! command -v scrcpy &> /dev/null; then
    echo "⚠️  Advertencia: scrcpy no está instalado"
    echo "   Instala con: sudo apt install scrcpy"
fi

# Verificar GTK
if ! python3 -c "import gi; gi.require_version('Gtk', '3.0')" 2>/dev/null; then
    echo "📦 Instalando dependencias de GTK..."
    sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
fi

echo "✨ Iniciando aplicación..."
echo ""

# Ejecutar aplicación
python3 miru-app.py
