
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import threading
from datetime import datetime
from ..core.device_manager import DeviceManager
from ..plugins.implementations import MirrorPlugin, RecordPlugin, ScreenshotPlugin, HIDPlugin, LogcatPlugin, RebootPlugin

class MiruMainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Miru - Android Development Suite")
        self.set_default_size(1000, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.device_manager = DeviceManager()
        self.plugins = [
            MirrorPlugin(),
            RecordPlugin(),
            ScreenshotPlugin(),
            HIDPlugin(),
            LogcatPlugin(),
            RebootPlugin()
        ]

        # Apply styles
        self.apply_custom_css()
        
        # State
        self.device_connected = False
        self.device_info = {}
        
        # UI
        self.create_ui()
        
        # Start monitoring
        self.start_device_monitoring()
        
    def apply_custom_css(self):
        css_provider = Gtk.CssProvider()
        css = b"""
        window { background-color: #1a1a2e; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; }
        .title { font-size: 24px; font-weight: bold; color: white; }
        .subtitle { font-size: 14px; color: rgba(255, 255, 255, 0.8); }
        .tool-button { padding: 15px; margin: 5px; border-radius: 10px; background: #16213e; border: 1px solid #667eea; color: white; font-size: 14px; }
        .tool-button:hover { background: #667eea; border-color: #764ba2; }
        .status-connected { background-color: #00f2fe; color: #1a1a2e; padding: 5px 15px; border-radius: 15px; font-weight: bold; }
        .status-disconnected { background-color: #f5576c; color: white; padding: 5px 15px; border-radius: 15px; font-weight: bold; }
        .info-card { background: #16213e; padding: 15px; margin: 5px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1); }
        .info-label { color: #a8b2d1; font-size: 11px; }
        .info-value { color: white; font-size: 16px; font-weight: bold; }
        .activity-log { background: #16213e; color: #a8b2d1; padding: 10px; font-family: monospace; font-size: 12px; }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Header
        header = self.create_header()
        main_box.pack_start(header, False, False, 0)
        
        # Scrollable Content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scrolled, True, True, 0)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        scrolled.add(content_box)
        
        # Tools Section
        tools_label = Gtk.Label()
        tools_label.set_markup('<span size="large" weight="bold" foreground="white">Herramientas Android</span>')
        tools_label.set_halign(Gtk.Align.START)
        content_box.pack_start(tools_label, False, False, 0)
        
        content_box.pack_start(self.create_tools_grid(), False, False, 0)
        
        # Device Info Section
        device_label = Gtk.Label()
        device_label.set_markup('<span size="large" weight="bold" foreground="white">Información del Dispositivo</span>')
        device_label.set_halign(Gtk.Align.START)
        content_box.pack_start(device_label, False, False, 10)
        
        self.device_info_box = self.create_device_info()
        content_box.pack_start(self.device_info_box, False, False, 0)
        
        # Log Section
        activity_label = Gtk.Label()
        activity_label.set_markup('<span size="large" weight="bold" foreground="white">Registro de Actividad</span>')
        activity_label.set_halign(Gtk.Align.START)
        content_box.pack_start(activity_label, False, False, 10)
        
        self.activity_log_view = self.create_activity_log()
        content_box.pack_start(self.activity_log_view, True, True, 0)

    def create_header(self):
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.get_style_context().add_class('header')
        header_box.set_margin_top(15)
        header_box.set_margin_bottom(15)
        header_box.set_margin_start(20)
        header_box.set_margin_end(20)
        
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
        
        self.status_label = Gtk.Label(label="Verificando...")
        self.status_label.get_style_context().add_class('status-disconnected')
        header_box.pack_end(self.status_label, False, False, 0)
        
        return header_box

    def create_tools_grid(self):
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(15)
        grid.set_column_homogeneous(True)
        
        for i, plugin in enumerate(self.plugins):
            row = i // 3
            col = i % 3
            button = self.create_tool_button(plugin)
            grid.attach(button, col, row, 1, 1)
            
        return grid

    def create_tool_button(self, plugin):
        button = Gtk.Button()
        button.get_style_context().add_class('tool-button')
        button.set_size_request(250, 100)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        icon = Gtk.Label()
        icon.set_markup(f'<span size="xx-large">{plugin.icon}</span>')
        box.pack_start(icon, False, False, 0)
        
        name = Gtk.Label()
        name.set_markup(f'<span weight="bold" size="large" foreground="white">{plugin.name}</span>')
        box.pack_start(name, False, False, 0)
        
        desc = Gtk.Label(label=plugin.description)
        desc.set_markup(f'<span foreground="#a8b2d1">{plugin.description}</span>')
        box.pack_start(desc, False, False, 0)
        
        button.add(box)
        # Pass self as context
        button.connect('clicked', lambda w: plugin.run(self))
        return button

    def create_device_info(self):
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
        self.log("Aplicación iniciada")
        return scrolled

    # Context Interface Methods
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        GLib.idle_add(self._append_log, log_message)

    def _append_log(self, message):
        end_iter = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end_iter, message)
        return False
        
    def show_error(self, message):
        self.log(f"✕ Error: {message}")
        # Note: Dialogs might need to be run on main thread if triggered from bg thread
        if threading.current_thread() is threading.main_thread():
            self._show_error_dialog(message)
        else:
            GLib.idle_add(self._show_error_dialog, message)

    def _show_error_dialog(self, message):
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
        return False

    def schedule_ui_update(self, callback):
        GLib.idle_add(callback)

    # Device Monitoring
    def start_device_monitoring(self):
        self.update_device_status()
        GLib.timeout_add_seconds(5, self.update_device_status)

    def update_device_status(self):
        selector = self.device_manager.get_device_selector()
        self.device_connected = (selector is not None)
        
        if self.device_connected:
            GLib.idle_add(self._update_status_connected)
            # Fetch info in background if needed, but for now we do it synchronously as it's quick usually,
            # or we could make DeviceManager async. Original was blocking in timeout but usually fast.
            info = self.device_manager.get_device_info(selector)
            if info:
                GLib.idle_add(self._update_device_info, info)
        else:
            GLib.idle_add(self._update_status_disconnected)
        return True

    def _update_status_connected(self):
        self.status_label.set_text("✓ Dispositivo Conectado")
        self.status_label.get_style_context().remove_class('status-disconnected')
        self.status_label.get_style_context().add_class('status-connected')
        return False

    def _update_status_disconnected(self):
        self.status_label.set_text("✕ Sin Dispositivo")
        self.status_label.get_style_context().remove_class('status-connected')
        self.status_label.get_style_context().add_class('status-disconnected')
        
        for box in self.device_info_box.get_children():
            for child in box.get_children():
                if isinstance(child, Gtk.Label) and child.get_name().startswith('value_'):
                    child.set_markup('<span foreground="white" weight="bold" size="large">--</span>')
        return False

    def _update_device_info(self, info):
        for box in self.device_info_box.get_children():
            for child in box.get_children():
                if isinstance(child, Gtk.Label):
                    name = child.get_name()
                    val = info.get({'value_modelo':'model', 'value_android':'version', 
                                   'value_batería':'battery', 'value_estado':'state'}.get(name))
                    if val:
                         child.set_markup(f'<span foreground="white" weight="bold" size="large">{val}</span>')
        return False
