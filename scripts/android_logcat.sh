#!/bin/bash

# Limpiar pantalla
clear
echo "🔍 === Android Error Monitor (Logcat) === 🔍"
echo "Esperando dispositivo..."
echo "(Conecta tu móvil USB)"

adb $MIRU_ADB_DEVICE wait-for-device

echo "✅ Dispositivo conectado."
echo "-----------------------------------------------------"
echo "👁️  Mostrando ERRORES y CRASHES en tiempo real..."
echo "❌ Presiona CTRL+C para salir."
echo "-----------------------------------------------------"

# Explicación del comando:
# -v color: Colorea la salida para mejorar legibilidad
# *:E : Muestra SOLO Errores y Fatal (Ignora Info/Debug que meten ruido)
# Si quisieras ver todo, cambia *:E por *:V
adb $MIRU_ADB_DEVICE logcat -v color *:E
