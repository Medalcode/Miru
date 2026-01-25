# Arquitectura de Miru V2

Se ha refactorizado la aplicación `miru-app.py` monolítica a una arquitectura modular y escalable (package `miru/`).

## Estructura de Directorios

```
miru/
├── __init__.py
├── main.py                 # Punto de entrada principal
├── core/                   # Lógica de negocio y servicios
│   ├── device_manager.py   # Gestión de conexión ADB y estado del dispositivo
│   └── config_manager.py   # Gestión de configuración persistente
├── ui/                     # Capa de presentación (GTK)
│   ├── main_window.py      # Ventana principal y componentes UI
│   └── styles.py           # (Opcional) Definiciones CSS
└── plugins/                # Sistema de plugins para herramientas
    ├── interface.py        # Definición de la interfaz MiruPlugin
    └── implementations.py  # Implementaciones (Mirror, Logcat, etc.)
```

## Ventajas de la Nueva Arquitectura

1.  **Modularidad**: Cada componente tiene una responsabilidad única.
2.  **Plugin System**: Añadir nuevas herramientas es tan fácil como crear una nueva clase que herede de `MiruPlugin` y añadirla a la lista. No es necesario modificar la lógica de la UI principal.
3.  **Separación de Responsabilidades**:
    - `core`: Solo se preocupa de datos y lógica (ADB).
    - `ui`: Solo se preocupa de pintar la interfaz.
    - `plugins`: Conectan la UI con scripts o lógica específica.
4.  **Mantenibilidad**: Es más fácil encontrar y arreglar bugs en archivos pequeños y específicos que en un archivo de 600 líneas.

## Cómo añadir una nueva herramienta

1.  Abre `miru/plugins/implementations.py` (o crea un nuevo archivo en `plugins/`).
2.  Crea una clase que herede de `MiruPlugin`.
3.  Implementa `name`, `icon`, `description` y el método `run(self, context)`.
4.  Registra el plugin en `miru/ui/main_window.py` dentro de la lista `self.plugins`.

## Ejecución

El script `miru-app.py` en la raíz ahora actúa como un lanzador que importa el paquete `miru`.

```bash
python3 miru-app.py
```
