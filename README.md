# Miru - Android Development Suite (Debian Linux)

**Miru** es una suite de herramientas ligeras diseñada para darle una segunda vida a dispositivos Android antiguos, convirtiéndolos en potentes herramientas de desarrollo y monitoreo.

Todo se ejecuta con **un simple doble clic**, sin necesidad de abrir terminales ni escribir comandos.

## 🚀 Instalación Rápida

Para instalar todas las herramientas, iconos y dependencias de una sola vez, abre una terminal en la carpeta del proyecto y ejecuta:

```bash
# 1. Instalar dependencias esenciales
sudo apt update && sudo apt install -y scrcpy adb libnotify-bin

# 2. Ejecutar el instalador automático
./setup.sh
```

Esto creará los iconos de acceso directo en tu **Escritorio** y en el **Menú de Aplicaciones**.

---

## 🛠️ Herramientas Incluidas

La suite consta de 6 herramientas especializadas, cada una optimizada para un flujo de trabajo específico:

### 1. 📱 Android Mirror (`android-mirror`)

La herramienta principal. Visualiza y controla tu dispositivo Android en tiempo real.

- **Optimizada:** Configurada para hardware antiguo (800px, 30fps) para evitar lag.
- **Portapapeles Bidireccional:** Copia en PC (`Ctrl+C`) y pega en Android (`Ctrl+V`).
- **Arrastrar y Soltar:** Arrastra un APK a la ventana para instalarlo automáticamente.
- **Modo Pasivo:** Apaga la pantalla del móvil para ahorrar batería y calor.

### 2. 🔴 Android Record (`android-record`)

Graba automáticamente todo lo que haces en el dispositivo.

- **Sin configuración:** Al abrirlo, empieza a grabar.
- **Visual:** Muestra un indicador blanco donde tocas la pantalla (útil para demos).
- **Guardado:** Los videos `.mp4` se guardan automáticamente en `~/Videos/Android_Recordings` con la fecha y hora.

### 3. 📸 Android Snap (`android-snap`)

Toma una captura de pantalla de alta calidad instantáneamente.

- **Un clic:** Sin menús. Doble clic al icono y listo.
- **Destino:** La imagen `.png` aparece inmediatamente en tu **Escritorio**.

### 4. ⌨️ Android Type (`android-type`)

Activa el modo de teclado físico (HID).

- **Escritura Rápida:** Tu teclado del PC actúa como un teclado USB real conectado al móvil.
- **Atajos:** Permite usar atajos de Android (como cambiar de app con `Alt+Tab`) directamente en el teléfono.
- **Ideal para:** Escribir largos textos, URLs o chatear.

### 5. 🐛 Android Debug (`android-debug`)

Monitor de errores en tiempo real "estilo Matrix".

- **Filtrado Inteligente:** Ignora el ruido y muestra **SOLO** los errores (`Error`) y cierres inesperados (`Fatal`).
- **Visual:** Abre una terminal dedicada con colores para detectar fallos al instante mientras pruebas tu app.

### 6. 🚑 Android Reset (`android-reset`)

Tu botón de pánico / kit de emergencia.

- **Inteligente:**
  - Si el móvil está conectado: Lo reinicia suavemente (`reboot`).
  - Si el móvil **NO** se detecta: Reinicia los drivers ADB del PC para arreglar problemas de conexión USB.

---

## 📂 Estructura del Proyecto

```text
Miru/
├── scripts/               # Lógica interna (Bash scripts)
│   ├── android_mirror.sh      # Core: Maneja Mirror, Record y Type
│   ├── android_screenshot.sh  # Core: Maneja Snap
│   ├── android_logcat.sh      # Core: Maneja Debug
│   └── android_reboot.sh      # Core: Maneja Reset
├── android-*.desktop      # Archivos de integración con el escritorio (Iconos)
├── setup.sh               # Instalador automatizado
└── README.md              # Este archivo
```

## 📋 Requisitos Previos

Esta suite se basa en herramientas estándar de código abierto:

- **Debian/Ubuntu/Linux Mint** (u otra distro basada en Debian).
- **ADB** (Android Debug Bridge).
- **Scrcpy** (Screen Copy).
- **Libnotify** (Para las notificaciones visuales de escritorio).

## 💡 Notas de Uso

- **Tecla MOD:** La tecla para atajos dentro de la ventana de espejo (como `Mod+f` para pantalla completa) es usualmente **Alt Izquierdo**.
- **Wi-Fi:** Todas las herramientas funcionan también por Wi-Fi si conectas el dispositivo previamente (`adb connect IP_DEL_MOVIL`).
