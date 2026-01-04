# Miru Project

Este proyecto contiene un conjunto de herramientas para visualizar y controlar dispositivos Android antiguos desde un PC con Debian Linux.

El objetivo es dar una "segunda vida" a teléfonos en desuso, permitiendo ver su actividad en un monitor de PC con un impacto mínimo en los recursos del teléfono.

## Contenido

- **scripts/android_mirror.sh**: Script principal de Bash que gestiona la conexión ADB y lanza `scrcpy` con parámetros optimizados.
- **android-mirror.desktop**: Archivo de entrada de escritorio para integración con menús de GNOME/KDE/XFCE.
- **INSTALL.md**: Guía paso a paso para configurar las dependencias del sistema y los accesos directos.

## Características

- **Detección Automática**: Espera a que el dispositivo se conecte.
- **Optimizado**: Configurado para bajo consumo de CPU/GPU (800px, 30fps, 2Mbps).
- **Modo Pasivo**: Apaga la pantalla del móvil automáticamente al conectar para evitar sobrecalentamiento (`-S` flag).
- **Notificaciones**: Integración con el sistema de notificaciones de escritorio de Linux.
