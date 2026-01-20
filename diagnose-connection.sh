#!/bin/bash

# Script de diagnóstico y solución de problemas de conexión ADB
# Miru - Android Development Suite

echo "🔍 Diagnóstico de Conexión ADB"
echo "================================"
echo ""

# 1. Verificar ADB instalado
echo "1️⃣  Verificando ADB..."
if command -v adb &> /dev/null; then
    echo "   ✅ ADB instalado: $(adb version | head -n1)"
else
    echo "   ❌ ADB no está instalado"
    echo "   💡 Instala con: sudo apt install adb"
    exit 1
fi
echo ""

# 2. Estado actual del servidor ADB
echo "2️⃣  Estado del servidor ADB..."
adb devices -l
echo ""

# 3. Detectar dispositivos duplicados u offline
echo "3️⃣  Analizando dispositivos..."
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "device")
OFFLINE_COUNT=$(adb devices | grep -c "offline")
UNAUTHORIZED_COUNT=$(adb devices | grep -c "unauthorized")

echo "   📱 Dispositivos conectados: $DEVICE_COUNT"
echo "   ⚠️  Dispositivos offline: $OFFLINE_COUNT"
echo "   🔒 Dispositivos no autorizados: $UNAUTHORIZED_COUNT"
echo ""

# 4. Solucionar problemas
if [ $OFFLINE_COUNT -gt 0 ] || [ $UNAUTHORIZED_COUNT -gt 0 ]; then
    echo "4️⃣  Detectados problemas de conexión. Solucionando..."
    echo ""
    
    # Reiniciar servidor ADB
    echo "   🔄 Reiniciando servidor ADB..."
    adb kill-server
    sleep 2
    adb start-server
    sleep 2
    echo ""
    
    # Verificar nuevamente
    echo "   📊 Estado después del reinicio:"
    adb devices -l
    echo ""
fi

# 5. Verificar depuración USB
echo "5️⃣  Verificando depuración USB..."
DEVICE_SERIAL=$(adb devices | grep -v "List" | grep "device" | head -n1 | awk '{print $1}')

if [ -n "$DEVICE_SERIAL" ]; then
    echo "   ✅ Dispositivo detectado: $DEVICE_SERIAL"
    
    # Obtener información del dispositivo
    echo ""
    echo "   📱 Información del dispositivo:"
    echo "   ├─ Modelo: $(adb -s $DEVICE_SERIAL shell getprop ro.product.model 2>/dev/null || echo 'No disponible')"
    echo "   ├─ Fabricante: $(adb -s $DEVICE_SERIAL shell getprop ro.product.manufacturer 2>/dev/null || echo 'No disponible')"
    echo "   ├─ Android: $(adb -s $DEVICE_SERIAL shell getprop ro.build.version.release 2>/dev/null || echo 'No disponible')"
    echo "   └─ Estado: $(adb -s $DEVICE_SERIAL get-state 2>/dev/null || echo 'No disponible')"
else
    echo "   ❌ No se detectó ningún dispositivo"
    echo ""
    echo "   💡 Soluciones sugeridas:"
    echo "   1. Desconecta y vuelve a conectar el cable USB"
    echo "   2. Verifica que la depuración USB esté activada en el teléfono"
    echo "   3. En el teléfono, ve a: Ajustes > Opciones de desarrollador > Depuración USB"
    echo "   4. Si aparece un diálogo en el teléfono, acepta 'Permitir depuración USB'"
    echo "   5. Prueba con otro puerto USB o cable"
fi

echo ""
echo "================================"
echo "✅ Diagnóstico completado"
echo ""

# 6. Sugerencias finales
if [ $DEVICE_COUNT -eq 0 ]; then
    echo "⚠️  NO HAY DISPOSITIVOS CONECTADOS"
    echo ""
    echo "📋 Checklist de solución:"
    echo "  □ Cable USB conectado correctamente"
    echo "  □ Depuración USB activada en el teléfono"
    echo "  □ Diálogo de autorización aceptado en el teléfono"
    echo "  □ Drivers USB instalados (si es necesario)"
    echo "  □ Puerto USB funcionando correctamente"
    echo ""
elif [ $DEVICE_COUNT -gt 1 ]; then
    echo "⚠️  MÚLTIPLES DISPOSITIVOS DETECTADOS"
    echo ""
    echo "💡 La aplicación usará el primer dispositivo disponible."
    echo "   Si quieres usar un dispositivo específico, desconecta los demás."
    echo ""
else
    echo "✅ TODO CORRECTO - Dispositivo listo para usar"
    echo ""
    echo "🚀 Puedes iniciar Miru con: ./start-app.sh"
    echo ""
fi
