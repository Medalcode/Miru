# Solución de Problemas de Conexión - Miru

## ❌ Problema: "No se conectó el teléfono"

### 🔍 Diagnóstico del Problema

El error se debía a que ADB detectaba **múltiples instancias del mismo dispositivo**:

- Una conexión en estado `offline` (puerto USB 1-7)
- Una conexión en estado `device` (puerto USB 1-8)

Esto causaba el error: **"error: more than one device/emulator"**

---

## ✅ Soluciones Implementadas

### 1. **Filtrado Inteligente de Dispositivos**

La aplicación ahora:

- ✅ Ignora dispositivos en estado `offline`
- ✅ Ignora dispositivos `unauthorized`
- ✅ Solo cuenta dispositivos en estado `device`

### 2. **Uso de Serial del Dispositivo**

Todos los comandos ADB ahora usan el flag `-s <serial>`:

```bash
adb -s ZE222GMD2B shell getprop ro.product.model
```

Esto evita el error "more than one device/emulator"

### 3. **Scripts de Diagnóstico**

Se crearon 2 scripts útiles:

#### `diagnose-connection.sh`

Diagnostica problemas de conexión:

```bash
./diagnose-connection.sh
```

Muestra:

- ✅ Estado de ADB
- 📱 Dispositivos conectados
- ⚠️ Dispositivos offline
- 🔒 Dispositivos no autorizados
- 📊 Información del dispositivo

#### `fix-connection.sh`

Soluciona problemas de conexión:

```bash
./fix-connection.sh
```

Te guía para:

1. Desconectar el cable USB
2. Esperar 3 segundos
3. Reconectar el cable
4. Reiniciar servidor ADB

---

## 🛠️ Soluciones Manuales

### Opción 1: Reiniciar Servidor ADB

```bash
adb kill-server
adb start-server
adb devices
```

### Opción 2: Reconectar el Dispositivo

1. Desconecta el cable USB del teléfono
2. Espera 5 segundos
3. Vuelve a conectar el cable
4. Acepta el diálogo de autorización si aparece

### Opción 3: Usar Otro Puerto USB

Si el problema persiste:

- Prueba conectar el cable en otro puerto USB de la PC
- Usa un cable USB diferente
- Evita usar hubs USB

### Opción 4: Verificar Depuración USB

En el teléfono:

1. Ve a **Ajustes** > **Acerca del teléfono**
2. Toca 7 veces en **Número de compilación**
3. Ve a **Ajustes** > **Opciones de desarrollador**
4. Activa **Depuración USB**
5. Si aparece un diálogo, marca "Permitir siempre" y acepta

---

## 🔍 Verificar Estado de la Conexión

### Ver dispositivos conectados:

```bash
adb devices -l
```

**Salida correcta:**

```
List of devices attached
ZE222GMD2B      device usb:1-8 product:astro_retail model:motorola_one_fusion
```

**Salida con problemas:**

```
List of devices attached
ZE222GMD2B      offline usb:1-7
ZE222GMD2B      device usb:1-8
```

### Obtener información del dispositivo:

```bash
SERIAL=$(adb devices | grep -v "List" | grep "device" | head -n1 | awk '{print $1}')
adb -s $SERIAL shell getprop ro.product.model
adb -s $SERIAL shell getprop ro.build.version.release
```

---

## ⚠️ Problemas Comunes

### "unauthorized"

**Causa:** No has aceptado el diálogo de depuración USB en el teléfono

**Solución:**

1. Desbloquea el teléfono
2. Busca el diálogo "Permitir depuración USB"
3. Marca "Permitir siempre desde esta computadora"
4. Toca "Permitir"

### "offline"

**Causa:** Conexión USB inestable o múltiples conexiones

**Solución:**

1. Desconecta y reconecta el cable
2. Usa otro puerto USB
3. Reinicia el servidor ADB

### "no permissions"

**Causa:** Problemas de permisos de udev

**Solución:**

```bash
sudo usermod -aG plugdev $USER
sudo apt install android-sdk-platform-tools-common
# Reinicia la sesión
```

### "device not found"

**Causa:** No hay dispositivo conectado

**Solución:**

1. Conecta el cable USB
2. Activa depuración USB
3. Verifica que el cable funcione (prueba con otro)

---

## 📊 Estado Actual

Después de las correcciones:

✅ **Aplicación actualizada** - Maneja múltiples dispositivos correctamente  
✅ **Filtrado inteligente** - Ignora dispositivos offline  
✅ **Uso de serial** - Evita conflictos con múltiples dispositivos  
✅ **Scripts de diagnóstico** - Facilitan la solución de problemas

---

## 🚀 Iniciar Miru

Una vez solucionado el problema de conexión:

```bash
./start-app.sh
```

La aplicación ahora debería:

- ✅ Detectar el dispositivo correctamente
- ✅ Mostrar "✓ Dispositivo Conectado" en el header
- ✅ Mostrar información del dispositivo (modelo, Android, batería)
- ✅ Permitir ejecutar todas las herramientas

---

## 💡 Consejos

1. **Usa siempre el mismo puerto USB** para evitar múltiples conexiones
2. **Marca "Permitir siempre"** en el diálogo de depuración USB
3. **Ejecuta `diagnose-connection.sh`** si tienes problemas
4. **Mantén el cable conectado** mientras usas las herramientas
5. **Evita hubs USB** - conecta directamente a la PC

---

## 📝 Logs Útiles

### Ver logs de ADB:

```bash
adb logcat | grep -i error
```

### Ver procesos de ADB:

```bash
ps aux | grep adb
```

### Matar todos los procesos de ADB:

```bash
killall adb
adb start-server
```

---

**Última actualización:** 2026-01-20  
**Estado:** ✅ Problema resuelto
