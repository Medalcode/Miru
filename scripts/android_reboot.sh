#!/bin/bash

# Enviar notificación de inicio
if command -v notify-send &> /dev/null; then
    notify-send "Android Reset" "Analizando estado..." --icon=system-reboot
fi

# Comprobar si hay dispositivo conectado
DEVICES=$(adb devices | grep -w "device")

if [ -n "$DEVICES" ]; then
    # CASO 1: Dispositivo encontrado -> Reiniciar el Teléfono
    if command -v notify-send &> /dev/null; then
        notify-send "Android Reset" "Reiniciando el teléfono..." --icon=system-reboot
    fi
    adb reboot
else
    # CASO 2: No hay dispositivo -> Reiniciar el Servidor ADB (Arregla bugs de conexión)
    if command -v notify-send &> /dev/null; then
        notify-send "Fix Connection" "No se detecta móvil. Reiniciando drivers ADB..." --icon=network-wired
    fi
    adb kill-server
    adb start-server
    
    if command -v notify-send &> /dev/null; then
        notify-send "Fix Connection" "Drivers reiniciados. Desconecta y reconecta el USB." --icon=network-wired
    fi
fi
