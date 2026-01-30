Bitacora
📌 Meta

Project: Miru

Owner: Medalcode

Repo: Medalcode/Miru

Started: 2025-01-01

LastUpdate: 2026-01-30

🧱 Features
[DONE] F-001 — Refactorización del Núcleo

Description: Se transformó el monolito miru-app.py en un paquete Python robusto (miru/). Implementación de DeviceManager para centralizar lógica ADB y ConfigManager para configuraciones persistentes.

Tags: core, refactoring, python, architecture

Completed: 2025-01-15

[DONE] F-002 — Sistema de Plugins

Description: Creación de arquitectura basada en plugins (miru/plugins/) para escalabilidad. Definición de interfaz MiruPlugin y migración de herramientas (Mirror, Record, Snap, HID, Debug, Reset).

Tags: plugins, architecture, scalability

Completed: 2025-01-20

[DONE] F-003 — Interfaz de Usuario

Description: Separación de la lógica de UI en miru/ui/main_window.py e integración dinámica de plugins en la interfaz.

Tags: ui, frontend, gtk

Completed: 2025-01-25

[DONE] F-004 — Limpieza y Organización

Description: Eliminación de accesos directos obsoletos y actualización de setup.sh. Actualización de miru-app.py y creación de ARCHITECTURE.md.

Tags: cleanup, documentation, maintenance

Completed: 2025-01-28

[TODO] F-005 — Gestor de Archivos

Description: Plugin para explorar, subir y bajar archivos del dispositivo.

Tags: feature, file-manager, plugin

[TODO] F-006 — Instalador de APKs

Description: Plugin para instalar APKs arrastrando y soltando (Drag & Drop).

Tags: feature, installer, ux

[TODO] F-007 — Configuración UI

Description: Interfaz gráfica para editar las preferencias (tema, rutas de grabación, parámetros de scrcpy).

Tags: feature, ui, settings

[TODO] F-008 — Manejo de Errores Async

Description: Mejorar la captura de errores en hilos secundarios para evitar bloqueos de UI.

Tags: technical, async, error-handling

[TODO] F-009 — Tests Unitarios

Description: Implementar pruebas para DeviceManager y parsing de salida ADB.

Tags: testing, qa, unit-tests

[TODO] F-010 — Soporte Multi-dispositivo UI

Description: Selector en la interfaz para cambiar entre múltiples dispositivos conectados 'on-the-fly'.

Tags: feature, ui, multi-device

[TODO] F-011 — Distribución (Empaquetado)

Description: Crear scripts para generar paquetes .deb o AppImage.

Tags: distribution, packaging, devops
