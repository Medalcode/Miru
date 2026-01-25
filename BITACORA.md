# Bitácora de Desarrollo - Miru

## ✅ Tareas Realizadas

### 📅 Enero 2025 - Refactorización Mayor a Arquitectura Modular

- **Refactorización del Núcleo:**
  - Se transformó el monolito `miru-app.py` en un paquete Python robusto (`miru/`).
  - Implementación de `DeviceManager` (`miru/core/device_manager.py`) para centralizar la lógica de conexión ADB y recuperación de información del dispositivo.
  - Implementación de `ConfigManager` (`miru/core/config_manager.py`) para manejar configuraciones persistentes (Singleton pattern).

- **Sistema de Plugins:**
  - Creación de una arquitectura basada en plugins (`miru/plugins/`) para facilitar la escalabilidad.
  - Definición de interfaz base `MiruPlugin`.
  - Migración de todas las herramientas existentes (Mirror, Record, Snap, HID, Debug, Reset) a plugins independientes.

- **Interfaz de Usuario:**
  - Separación de la lógica de UI en `miru/ui/main_window.py`.
  - Integración dinámica de plugins en la interfaz.

- **Limpieza y Organización:**
  - Eliminación de accesos directos individuales obsoletos (`android-*.desktop`).
  - Actualización de `setup.sh` para instalar el lanzador unificado y limpiar residuos legacy.
  - `miru-app.py` actualizado para funcionar como entry-point ligero.
  - Creación de `ARCHITECTURE.md` documentando el nuevo diseño.

## 📝 Tareas Pendientes

### Funcionalidades

- [ ] **Gestor de Archivos:** Plugin para explorar, subir y bajar archivos del dispositivo.
- [ ] **Instalador de APKs:** Plugin para instalar APKs arrastrando y soltando (Drag & Drop).
- [ ] **Configuración UI:** Interfaz gráfica para editar las preferencias (tema, rutas de grabación, parámetros de scrcpy).

### Mejoras Técnicas

- [ ] **Manejo de Errores Async:** Mejorar la captura de errores en hilos secundarios para evitar bloqueos de UI.
- [ ] **Tests Unitarios:** Implementar pruebas para `DeviceManager` y parsing de salida ADB.
- [ ] **Soporte Multi-dispositivo UI:** Selector en la interfaz para cambiar entre múltiples dispositivos conectados 'on-the-fly'.

### Distribución

- [ ] **Empaquetado:** Crear scripts para generar .deb o AppImage.
