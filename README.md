# Miru - Android Development Suite (Nativa Linux) 📱🐧

**Miru** es una suite de herramientas nativa para Linux diseñada para darle una segunda vida a tus dispositivos Android, convirtiéndolos en potentes herramientas de monitoreo y desarrollo con un solo clic.

Esta versión ha sido completamente rediseñada como una **aplicación nativa GTK**, eliminando la necesidad de múltiples accesos directos y centralizando todo en una interfaz moderna y eficiente.

---

## 🚀 Instalación Rápida

### 1. Dependencias del Sistema

Instala las herramientas esenciales (ADB, Scrcpy y librerías GTK):

```bash
sudo apt update && sudo apt install -y scrcpy adb libnotify-bin python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### 2. Clonar y Ejecutar

```bash
git clone https://github.com/Medalcode/Miru.git
cd Miru
chmod +x start-app.sh
./start-app.sh
```

---

## 🛠️ Herramientas Integradas

La suite unificada incluye 6 funciones críticas:

1.  **📱 Android Mirror:** Proyecta y controla tu dispositivo en tiempo real. Optimizado para fluidez.
2.  **🔴 Android Record:** Graba la pantalla automáticamente con indicadores visuales de toque (ideal para demos).
3.  **📸 Android Snap:** Captura de pantalla instantánea guardada directamente en tu Escritorio.
4.  **⌨️ Android Type:** Utiliza tu teclado físico del PC como si fuera un teclado USB conectado al móvil (HID).
5.  **🐛 Android Debug:** Monitor Logcat en tiempo real filtrado para mostrar solo Errores y Fallos críticos.
6.  **🚑 Android Reset:** Botón de pánico para reiniciar el teléfono o resetear el servidor ADB si hay problemas.

---

## ✨ Características Premium (Versión Nativa)

- **Detección Inteligente:** Maneja automáticamente dispositivos "offline" o conexiones duplicadas.
- **Identificación por Puerto:** Diferencia dispositivos con el mismo serial usando el ID de transporte o puerto USB.
- **Monitoreo en Tiempo Real:** Visualiza Modelo, Versión de Android y Nivel de Batería al instante.
- **Registro de Actividad:** Historial detallado de todas las acciones realizadas.
- **Interfaz Moderna:** Diseño oscuro con gradientes, optimizado para flujos de trabajo de desarrollo.

---

## 🔧 Solución de Problemas (ADB)

Si tu dispositivo no aparece o dice "offline", hemos incluido herramientas automáticas de reparación:

- **`./diagnose-connection.sh`**: Escaneo detallado de la conexión.
- **`./fix-connection.sh`**: Asistente interactivo para resetear el enlace físico.
- **`./clean-adb.sh`**: Limpieza total de configuración y llaves ADB.

> Ver más información en [TROUBLESHOOTING.md](./TROUBLESHOOTING.md).

---

## 📂 Estructura del Proyecto

- `miru-app.py`: El corazón de la aplicación nativa (GTK3).
- `scripts/`: Lógica interna en Bash optimizada.
- `start-app.sh`: Lanzador inteligente con verificación de dependencias.
- `miru-app.desktop`: Integración para el menú de aplicaciones de Linux.

---

**Miru** | Desarrollado por **Medalcode** para una productividad Android sin fricciones. 🚀
