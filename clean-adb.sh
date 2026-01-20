#!/bin/bash

# Script para desconectar el dispositivo offline permanentemente
# Esto fuerza a ADB a olvidar la conexión offline

echo "🔧 Solucionando conexión offline permanentemente..."
echo ""

# Matar servidor ADB
echo "1️⃣  Deteniendo servidor ADB..."
adb kill-server
sleep 2

# Limpiar configuración de ADB
echo "2️⃣  Limpiando configuración de ADB..."
rm -f ~/.android/adbkey ~/.android/adbkey.pub 2>/dev/null
rm -rf ~/.android/adb* 2>/dev/null

# Reiniciar servidor
echo "3️⃣  Reiniciando servidor ADB..."
adb start-server
sleep 3

echo ""
echo "4️⃣  Estado actual:"
adb devices -l

echo ""
echo "================================"

# Contar dispositivos
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep "\tdevice" | wc -l)
OFFLINE_COUNT=$(adb devices | grep -c "offline")

if [ $OFFLINE_COUNT -gt 0 ]; then
    echo "⚠️  Aún hay dispositivos offline"
    echo ""
    echo "💡 SOLUCIÓN DEFINITIVA:"
    echo "   El dispositivo está conectado en 2 puertos USB diferentes."
    echo "   Necesitas DESCONECTAR FÍSICAMENTE uno de los cables:"
    echo ""
    echo "   Opción 1: Desconecta el cable del puerto USB 1-7 (offline)"
    echo "   Opción 2: Usa solo UN cable USB para conectar el teléfono"
    echo ""
    echo "   Después de desconectar, ejecuta:"
    echo "   ./start-app.sh"
else
    echo "✅ ¡Problema resuelto! Solo hay un dispositivo conectado"
    echo ""
    echo "🚀 Puedes iniciar Miru con: ./start-app.sh"
fi
