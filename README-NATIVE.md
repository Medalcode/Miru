# Miru - Android Development Suite (Aplicación Nativa Linux)

**Miru** es una **aplicación nativa de Linux con interfaz GTK** que integra todas las herramientas de desarrollo Android en una sola ventana.

## 🎯 Aplicación Nativa vs Web

Esta es una **aplicación de escritorio real** para Linux, no una aplicación web:

| Característica  | Aplicación Nativa               |
| --------------- | ------------------------------- |
| **Tecnología**  | Python + GTK3                   |
| **Tipo**        | Aplicación de escritorio nativa |
| **Integración** | Completa con el sistema Linux   |
| **Rendimiento** | Nativo, sin navegador           |
| **Apariencia**  | Tema GTK del sistema            |

## 🚀 Instalación Rápida

### 1. Instalar Dependencias del Sistema

```bash
sudo apt update && sudo apt install -y \
    scrcpy \
    adb \
    libnotify-bin \
    python3 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0
```

### 2. Iniciar la Aplicación

```bash
./start-app.sh
```

O hacer doble clic en el archivo `miru-app.desktop`

## ✨ Características

### 🖥️ Aplicación Nativa GTK

- **Ventana nativa** de Linux (no navegador)
- **Integración completa** con el escritorio
- **Tema del sistema** automático
- **Rendimiento óptimo** sin overhead de navegador

### 📱 Todas las Herramientas Integradas

- **🪞 Android Mirror** - Control en tiempo real
- **🔴 Android Record** - Grabación de pantalla
- **📸 Android Snap** - Capturas instantáneas
- **⌨️ Android Type** - Modo teclado HID
- **🐛 Android Debug** - Monitor de logs
- **🚑 Android Reset** - Reinicio y recuperación

### 📊 Monitoreo en Tiempo Real

- Estado de conexión del dispositivo
- Información completa (modelo, Android, batería, estado)
- Registro de actividad con timestamps
- Actualización automática cada 5 segundos

### 🎨 Interfaz Moderna

- Diseño oscuro con gradientes púrpura
- Tarjetas organizadas en grid
- Iconos emoji grandes y claros
- Scroll suave en el log de actividad

## 📂 Estructura del Proyecto

```text
Miru/
├── miru-app.py            # Aplicación principal GTK
├── start-app.sh           # Launcher de la aplicación
├── miru-app.desktop       # Acceso directo de escritorio
├── requirements.txt       # Dependencias Python
├── scripts/               # Scripts bash originales
│   ├── android_mirror.sh
│   ├── android_screenshot.sh
│   ├── android_logcat.sh
│   └── android_reboot.sh
└── README-NATIVE.md       # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Python 3** - Lenguaje de programación
- **GTK 3** - Toolkit de interfaz gráfica
- **PyGObject** - Bindings de Python para GTK
- **ADB** - Android Debug Bridge
- **Scrcpy** - Screen Copy para Android

## 🎯 Ventajas de la Aplicación Nativa

✅ **Rendimiento superior** - Sin overhead de navegador  
✅ **Integración completa** - Usa el tema del sistema  
✅ **Menor consumo** - Menos RAM y CPU  
✅ **Más rápida** - Inicio instantáneo  
✅ **Offline** - No necesita servidor web  
✅ **Nativa** - Se siente como parte del sistema

## 📋 Uso

### Iniciar desde Terminal

```bash
cd /home/medalcode/Documentos/GitHub/Miru
./start-app.sh
```

### Crear Acceso Directo en el Escritorio

```bash
cp miru-app.desktop ~/Escritorio/
chmod +x ~/Escritorio/miru-app.desktop
```

### Añadir al Menú de Aplicaciones

```bash
cp miru-app.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

## 🎨 Personalización

La aplicación usa CSS interno para los estilos. Puedes modificar los colores editando la función `apply_custom_css()` en `miru-app.py`:

```python
css = b"""
window {
    background-color: #1a1a2e;  # Cambiar color de fondo
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  # Cambiar gradiente
}
"""
```

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
python3 miru-app.py
```

### Depurar

La aplicación imprime información de debug en la consola. Ejecuta desde terminal para ver los mensajes.

### Añadir nuevas herramientas

1. Añade el botón en `create_tools_grid()`
2. Crea el método `run_<nombre>()`
3. Conecta el botón con el método

## 🐛 Troubleshooting

### La aplicación no inicia

```bash
# Verificar GTK
python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk"

# Reinstalar dependencias
sudo apt install --reinstall python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### No detecta el dispositivo

```bash
# Verificar ADB
adb devices

# Reiniciar servidor ADB
adb kill-server
adb start-server
```

### Warning sobre temas

El warning `Theme file for breeze_cursors has no directories` es inofensivo y no afecta la funcionalidad.

## 📝 Diferencias con la Versión Web

| Aspecto     | Nativa (GTK)             | Web (Flask)     |
| ----------- | ------------------------ | --------------- |
| Tecnología  | Python + GTK             | HTML + CSS + JS |
| Ejecución   | Aplicación de escritorio | Navegador web   |
| Servidor    | No necesita              | Requiere Flask  |
| Rendimiento | Más rápido               | Más lento       |
| Integración | Completa con Linux       | Limitada        |
| Acceso      | Local                    | Local o remoto  |

## 🚀 Próximas Mejoras

- [ ] Soporte para múltiples dispositivos
- [ ] Configuración de scrcpy desde la UI
- [ ] Instalador de APKs con drag & drop
- [ ] Terminal ADB integrada
- [ ] Temas personalizables
- [ ] Notificaciones del sistema

---

**Miru Native** - Aplicación de escritorio Linux para desarrollo Android 🐧📱
