#!/bin/bash

# Script para limpiar conexiones ADB duplicadas y offline
# Miru - Android Development Suite

echo "🧹 Limpiando conexiones ADB..."
echo ""

# Desconectar el teléfono físicamente por un momento
echo "📱 Por favor:"
echo "   1. DESCONECTA el cable USB del teléfono"
echo "   2. Espera 3 segundos"
echo "   3. VUELVE A CONECTAR el cable USB"
echo ""
echo "Presiona ENTER cuando hayas reconectado el cable..."
read

echo ""
echo "🔄 Reiniciando servidor ADB..."
adb kill-server
sleep 2
adb start-server
sleep 2

echo ""
echo "📊 Estado de la conexión:"
adb devices -l

echo ""
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "\tdevice")

if [ $DEVICE_COUNT -eq 1 ]; then
    echo "✅ ¡Perfecto! Dispositivo conectado correctamente"
    
    # Obtener información
    DEVICE_SERIAL=$(adb devices | grep -v "List" | grep "\tdevice" | head -n1 | awk '{print $1}')
    echo ""
    echo "📱 Dispositivo: $DEVICE_SERIAL"
    echo "   Modelo: $(adb -s $DEVICE_SERIAL shell getprop ro.product.model 2>/dev/null)"
    echo "   Android: $(adb -s $DEVICE_SERIAL shell getprop ro.build.version.release 2>/dev/null)"
    echo ""
    echo "🚀 Ahora puedes iniciar Miru"
elif [ $DEVICE_COUNT -eq 0 ]; then
    echo "❌ No se detectó ningún dispositivo"
    echo ""
    echo "💡 Verifica:"
    echo "   - Cable USB conectado correctamente"
    echo "   - Depuración USB activada en el teléfono"
    echo "   - Acepta el diálogo de autorización si aparece"
else
    echo "⚠️  Aún hay múltiples conexiones ($DEVICE_COUNT dispositivos)"
    echo ""
    echo "💡 Intenta:"
    echo "   1. Usar otro puerto USB"
    echo "   2. Usar otro cable USB"
    echo "   3. Reiniciar el teléfono"
fi
