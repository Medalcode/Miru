#!/usr/bin/env python3
"""
Miru - Android Development Suite
Aplicación nativa de Linux con interfaz GTK
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import subprocess
import os
import re
from datetime import datetime
import threading

# Rutas de scripts
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class MiruApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Miru - Android Development Suite")
        self.set_default_size(1000, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Aplicar CSS personalizado
        self.apply_custom_css()
        
        # Variables de estado
        self.device_connected = False
        self.device_info = {}
        
        # Crear interfaz
        self.create_ui()
        
        # Iniciar monitoreo de dispositivo
        self.start_device_monitoring()
        
    def apply_custom_css(self):
        """Aplica estilos CSS personalizados"""
        css_provider = Gtk.CssProvider()
        css = b"""
        window {
            background-color: #1a1a2e;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: white;
        }
        
        .title {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }
        
        .subtitle {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .tool-button {
            padding: 15px;
            margin: 5px;
            border-radius: 10px;
            background: #16213e;
            border: 1px solid #667eea;
            color: white;
            font-size: 14px;
        }
        
        .tool-button:hover {
            background: #667eea;
            border-color: #764ba2;
        }
        
        .status-connected {
            background-color: #00f2fe;
            color: #1a1a2e;
            padding: 5px 15px;
            border-radius: 15px;
            font-weight: bold;
        }
        
        .status-disconnected {
            background-color: #f5576c;
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-weight: bold;
        }
        
        .info-card {
            background: #16213e;
            padding: 15px;
            margin: 5px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .info-label {
            color: #a8b2d1;
            font-size: 11px;
        }
        
        .info-value {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        
        .activity-log {
            background: #16213e;
            color: #a8b2d1;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
        }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Header
        header = self.create_header()
        main_box.pack_start(header, False, False, 0)
        
        # Contenido principal con scroll
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scrolled, True, True, 0)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        scrolled.add(content_box)
        
        # Sección de herramientas
        tools_label = Gtk.Label()
        tools_label.set_markup('<span size="large" weight="bold" foreground="white">Herramientas Android</span>')
        tools_label.set_halign(Gtk.Align.START)
        content_box.pack_start(tools_label, False, False, 0)
        
        # Grid de herramientas
        tools_grid = self.create_tools_grid()
        content_box.pack_start(tools_grid, False, False, 0)
        
        # Información del dispositivo
        device_label = Gtk.Label()
        device_label.set_markup('<span size="large" weight="bold" foreground="white">Información del Dispositivo</span>')
        device_label.set_halign(Gtk.Align.START)
        content_box.pack_start(device_label, False, False, 10)
        
        self.device_info_box = self.create_device_info()
        content_box.pack_start(self.device_info_box, False, False, 0)
        
        # Log de actividad
        activity_label = Gtk.Label()
        activity_label.set_markup('<span size="large" weight="bold" foreground="white">Registro de Actividad</span>')
        activity_label.set_halign(Gtk.Align.START)
        content_box.pack_start(activity_label, False, False, 10)
        
        self.activity_log = self.create_activity_log()
        content_box.pack_start(self.activity_log, True, True, 0)
        
    def create_header(self):
        """Crea el header de la aplicación"""
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.get_style_context().add_class('header')
        header_box.set_margin_top(15)
        header_box.set_margin_bottom(15)
        header_box.set_margin_start(20)
        header_box.set_margin_end(20)
        
        # Logo y título
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        title = Gtk.Label()
        title.set_markup('<span size="xx-large" weight="bold">📱 Miru</span>')
        title.get_style_context().add_class('title')
        title.set_halign(Gtk.Align.START)
        title_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(label="Android Development Suite")
        subtitle.get_style_context().add_class('subtitle')
        subtitle.set_halign(Gtk.Align.START)
        title_box.pack_start(subtitle, False, False, 0)
        
        header_box.pack_start(title_box, True, True, 0)
        
        # Estado de conexión
        self.status_label = Gtk.Label(label="Verificando...")
        self.status_label.get_style_context().add_class('status-disconnected')
        header_box.pack_end(self.status_label, False, False, 0)
        
        return header_box
    
    def create_tools_grid(self):
        """Crea la grilla de herramientas"""
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(15)
        grid.set_column_homogeneous(True)
        
        tools = [
            {
                'icon': '🪞',
                'name': 'Android Mirror',
                'desc': 'Control en tiempo real',
                'action': self.run_mirror
            },
            {
                'icon': '🔴',
                'name': 'Android Record',
                'desc': 'Grabar pantalla',
                'action': self.run_record
            },
            {
                'icon': '📸',
                'name': 'Android Snap',
                'desc': 'Captura de pantalla',
                'action': self.run_screenshot
            },
            {
                'icon': '⌨️',
                'name': 'Android Type',
                'desc': 'Modo teclado HID',
                'action': self.run_hid
            },
            {
                'icon': '🐛',
                'name': 'Android Debug',
                'desc': 'Monitor de logs',
                'action': self.run_logcat
            },
            {
                'icon': '🚑',
                'name': 'Android Reset',
                'desc': 'Reiniciar dispositivo',
                'action': self.run_reboot
            }
        ]
        
        for i, tool in enumerate(tools):
            row = i // 3
            col = i % 3
            button = self.create_tool_button(tool)
            grid.attach(button, col, row, 1, 1)
        
        return grid
    
    def create_tool_button(self, tool):
        """Crea un botón de herramienta"""
        button = Gtk.Button()
        button.get_style_context().add_class('tool-button')
        button.set_size_request(250, 100)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        icon = Gtk.Label()
        icon.set_markup(f'<span size="xx-large">{tool["icon"]}</span>')
        box.pack_start(icon, False, False, 0)
        
        name = Gtk.Label()
        name.set_markup(f'<span weight="bold" size="large" foreground="white">{tool["name"]}</span>')
        box.pack_start(name, False, False, 0)
        
        desc = Gtk.Label(label=tool['desc'])
        desc.set_markup(f'<span foreground="#a8b2d1">{tool["desc"]}</span>')
        box.pack_start(desc, False, False, 0)
        
        button.add(box)
        button.connect('clicked', lambda w: tool['action']())
        
        return button
    
    def create_device_info(self):
        """Crea la sección de información del dispositivo"""
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_column_homogeneous(True)
        
        self.model_label = self.create_info_card("Modelo", "--")
        self.version_label = self.create_info_card("Android", "--")
        self.battery_label = self.create_info_card("Batería", "--")
        self.state_label = self.create_info_card("Estado", "--")
        
        grid.attach(self.model_label, 0, 0, 1, 1)
        grid.attach(self.version_label, 1, 0, 1, 1)
        grid.attach(self.battery_label, 2, 0, 1, 1)
        grid.attach(self.state_label, 3, 0, 1, 1)
        
        return grid
    
    def create_info_card(self, label, value):
        """Crea una tarjeta de información"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.get_style_context().add_class('info-card')
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        label_widget = Gtk.Label()
        label_widget.set_markup(f'<span foreground="#a8b2d1" size="small">{label.upper()}</span>')
        label_widget.set_halign(Gtk.Align.START)
        box.pack_start(label_widget, False, False, 0)
        
        value_widget = Gtk.Label()
        value_widget.set_markup(f'<span foreground="white" weight="bold" size="large">{value}</span>')
        value_widget.set_halign(Gtk.Align.START)
        value_widget.set_name(f'value_{label.lower()}')
        box.pack_start(value_widget, False, False, 0)
        
        return box
    
    def create_activity_log(self):
        """Crea el log de actividad"""
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_size_request(-1, 200)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.log_buffer = Gtk.TextBuffer()
        text_view = Gtk.TextView(buffer=self.log_buffer)
        text_view.set_editable(False)
        text_view.set_cursor_visible(False)
        text_view.get_style_context().add_class('activity-log')
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        
        scrolled.add(text_view)
        
        self.add_log("Aplicación iniciada")
        
        return scrolled
    
    def add_log(self, message):
        """Añade un mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        GLib.idle_add(self._append_log, log_message)
    
    def _append_log(self, message):
        """Añade texto al buffer (thread-safe)"""
        end_iter = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end_iter, message)
        return False
    
    def get_device_serial(self):
        """Obtiene el identificador único del dispositivo (prefiere USB path o transport_id)"""
        try:
            result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True, timeout=5)
            output = result.stdout
            
            for line in output.split('\n'):
                if 'List of devices' in line or not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    state = parts[1]
                    
                    if state == 'device':
                        # Preferir USB path si está disponible (formato usb:X-Y)
                        for part in parts:
                            if part.startswith('usb:'):
                                print(f"Using device via USB path: {part}")
                                return f"-s {part}"
                        
                        # Si no hay USB path, intentar transport_id
                        for part in parts:
                            if part.startswith('transport_id:'):
                                tid = part.split(':')[1]
                                print(f"Using device with transport_id: {tid}")
                                return f"-t {tid}"
                        
                        # Fallback al serial
                        print(f"Using device with serial: {serial}")
                        return f"-s {serial}"
            
            return None
        except Exception as e:
            print(f"Error getting device serial: {e}")
            return None
    
    def check_device(self):
        """Verifica si hay un dispositivo conectado"""
        return self.get_device_serial() is not None
    
    def get_device_info(self):
        """Obtiene información del dispositivo"""
        if not self.device_connected:
            return None
        
        device_selector = self.get_device_serial()
        if not device_selector:
            return None
        
        # Split device selector into flag and value
        selector_parts = device_selector.split()  # e.g., ['-t', '1'] or ['-s', 'SERIAL']
        
        try:
            # Modelo
            model = subprocess.run(
                ['adb'] + selector_parts + ['shell', 'getprop', 'ro.product.model'],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            
            # Versión Android
            version = subprocess.run(
                ['adb'] + selector_parts + ['shell', 'getprop', 'ro.build.version.release'],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            
            # Batería
            battery_output = subprocess.run(
                ['adb'] + selector_parts + ['shell', 'dumpsys', 'battery'],
                capture_output=True, text=True, timeout=5
            ).stdout
            battery_match = re.search(r'level: (\d+)', battery_output)
            battery = f"{battery_match.group(1)}%" if battery_match else "--"
            
            # Estado
            state = subprocess.run(
                ['adb'] + selector_parts + ['get-state'],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            
            return {
                'model': model,
                'version': version,
                'battery': battery,
                'state': state
            }
        except Exception as e:
            print(f"Error getting device info: {e}")
            return None
    
    def update_device_status(self):
        """Actualiza el estado del dispositivo en la UI"""
        self.device_connected = self.check_device()
        
        if self.device_connected:
            GLib.idle_add(self._update_status_connected)
            info = self.get_device_info()
            if info:
                GLib.idle_add(self._update_device_info, info)
        else:
            GLib.idle_add(self._update_status_disconnected)
        
        return True  # Continuar el timeout
    
    def _update_status_connected(self):
        """Actualiza UI cuando está conectado"""
        self.status_label.set_text("✓ Dispositivo Conectado")
        self.status_label.get_style_context().remove_class('status-disconnected')
        self.status_label.get_style_context().add_class('status-connected')
        return False
    
    def _update_status_disconnected(self):
        """Actualiza UI cuando está desconectado"""
        self.status_label.set_text("✕ Sin Dispositivo")
        self.status_label.get_style_context().remove_class('status-connected')
        self.status_label.get_style_context().add_class('status-disconnected')
        
        # Limpiar info del dispositivo
        for box in self.device_info_box.get_children():
            for child in box.get_children():
                if isinstance(child, Gtk.Label) and child.get_name().startswith('value_'):
                    child.set_markup('<span foreground="white" weight="bold" size="large">--</span>')
        
        return False
    
    def _update_device_info(self, info):
        """Actualiza la información del dispositivo"""
        for box in self.device_info_box.get_children():
            for child in box.get_children():
                if isinstance(child, Gtk.Label):
                    name = child.get_name()
                    if name == 'value_modelo':
                        child.set_markup(f'<span foreground="white" weight="bold" size="large">{info["model"]}</span>')
                    elif name == 'value_android':
                        child.set_markup(f'<span foreground="white" weight="bold" size="large">{info["version"]}</span>')
                    elif name == 'value_batería':
                        child.set_markup(f'<span foreground="white" weight="bold" size="large">{info["battery"]}</span>')
                    elif name == 'value_estado':
                        child.set_markup(f'<span foreground="white" weight="bold" size="large">{info["state"]}</span>')
        return False
    
    def start_device_monitoring(self):
        """Inicia el monitoreo del dispositivo"""
        # Primera actualización inmediata
        self.update_device_status()
        
        # Actualizar cada 5 segundos
        GLib.timeout_add_seconds(5, self.update_device_status)
    
    def _get_script_env(self):
        """Genera el entorno con las variables necesarias para los scripts"""
        env = os.environ.copy()
        selector = self.get_device_serial()
        if selector:
            env['MIRU_ADB_DEVICE'] = selector
            # También exportamos ANDROID_SERIAL por si los scripts o scrcpy lo usan directamente
            if selector.startswith('-s '):
                env['ANDROID_SERIAL'] = selector[3:]
        return env
    
    # Métodos para ejecutar herramientas
    def run_mirror(self):
        """Ejecuta Android Mirror"""
        if not self.device_connected:
            self.show_error("No hay dispositivo conectado")
            return
        
        self.add_log("▶ Ejecutando Android Mirror")
        script = os.path.join(SCRIPTS_DIR, 'android_mirror.sh')
        subprocess.Popen(['bash', script, 'mirror'], env=self._get_script_env())
    
    def run_record(self):
        """Ejecuta Android Record"""
        if not self.device_connected:
            self.show_error("No hay dispositivo conectado")
            return
        
        self.add_log("▶ Ejecutando Android Record")
        script = os.path.join(SCRIPTS_DIR, 'android_mirror.sh')
        subprocess.Popen(['bash', script, 'record'], env=self._get_script_env())
    
    def run_screenshot(self):
        """Ejecuta Android Screenshot"""
        if not self.device_connected:
            self.show_error("No hay dispositivo conectado")
            return
        
        self.add_log("▶ Ejecutando Android Snap")
        script = os.path.join(SCRIPTS_DIR, 'android_screenshot.sh')
        threading.Thread(target=self._run_screenshot_thread, args=(script,), daemon=True).start()
    
    def _run_screenshot_thread(self, script):
        """Ejecuta screenshot en thread separado"""
        try:
            result = subprocess.run(['bash', script], capture_output=True, timeout=10, env=self._get_script_env())
            if result.returncode == 0:
                GLib.idle_add(lambda: self.add_log("✓ Captura guardada en el Escritorio"))
            else:
                GLib.idle_add(lambda: self.add_log("✕ Error al capturar pantalla"))
        except Exception as e:
            GLib.idle_add(lambda: self.add_log(f"✕ Error: {str(e)}"))
    
    def run_hid(self):
        """Ejecuta Android HID"""
        if not self.device_connected:
            self.show_error("No hay dispositivo conectado")
            return
        
        self.add_log("▶ Ejecutando Android Type (HID)")
        script = os.path.join(SCRIPTS_DIR, 'android_mirror.sh')
        subprocess.Popen(['bash', script, 'hid'], env=self._get_script_env())
    
    def run_logcat(self):
        """Ejecuta Android Logcat"""
        if not self.device_connected:
            self.show_error("No hay dispositivo conectado")
            return
        
        self.add_log("▶ Ejecutando Android Debug")
        script = os.path.join(SCRIPTS_DIR, 'android_logcat.sh')
        subprocess.Popen(['bash', script], env=self._get_script_env())
    
    def run_reboot(self):
        """Ejecuta Android Reboot"""
        self.add_log("▶ Ejecutando Android Reset")
        script = os.path.join(SCRIPTS_DIR, 'android_reboot.sh')
        threading.Thread(target=self._run_reboot_thread, args=(script,), daemon=True).start()
    
    def _run_reboot_thread(self, script):
        """Ejecuta reboot en thread separado"""
        try:
            result = subprocess.run(['bash', script], capture_output=True, timeout=30, env=self._get_script_env())
            if result.returncode == 0:
                GLib.idle_add(lambda: self.add_log("✓ Reinicio completado"))
            else:
                GLib.idle_add(lambda: self.add_log("✕ Error al reiniciar"))
        except Exception as e:
            GLib.idle_add(lambda: self.add_log(f"✕ Error: {str(e)}"))
    
    def show_error(self, message):
        """Muestra un diálogo de error"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
        self.add_log(f"✕ Error: {message}")

def main():
    app = MiruApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
