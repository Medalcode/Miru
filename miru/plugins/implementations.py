
import os
import subprocess
import threading
from .interface import MiruPlugin
from ..core.device_manager import DeviceManager

# Helper to find scripts dir relative to this file
# Assumed structure:
# root/
#   scripts/
#   miru/
#     plugins/
#       implementations.py
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts'))

class BaseScriptPlugin(MiruPlugin):
    """Plugin base que ejecuta un script de bash"""
    def __init__(self):
        self.device_manager = DeviceManager()

    def _get_script_path(self, script_name):
        return os.path.join(SCRIPTS_DIR, script_name)

    def _check_connection(self, context):
        if not self.device_manager.get_device_selector():
            context.show_error("No hay dispositivo conectado")
            return False
        return True

    def _execute_subprocess(self, cmd, context):
         subprocess.Popen(cmd, env=self.device_manager.get_env_for_scripts())

class MirrorPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Mirror"
    @property
    def icon(self): return "🪞"
    @property
    def description(self): return "Control en tiempo real"

    def run(self, context):
        if not self._check_connection(context): return
        context.log("▶ Ejecutando Android Mirror")
        script = self._get_script_path('android_mirror.sh')
        self._execute_subprocess(['bash', script, 'mirror'], context)

class RecordPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Record"
    @property
    def icon(self): return "🔴"
    @property
    def description(self): return "Grabar pantalla"

    def run(self, context):
        if not self._check_connection(context): return
        context.log("▶ Ejecutando Android Record")
        script = self._get_script_path('android_mirror.sh')
        self._execute_subprocess(['bash', script, 'record'], context)

class HIDPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Type"
    @property
    def icon(self): return "⌨️"
    @property
    def description(self): return "Modo teclado HID"

    def run(self, context):
        if not self._check_connection(context): return
        context.log("▶ Ejecutando Android Type (HID)")
        script = self._get_script_path('android_mirror.sh')
        self._execute_subprocess(['bash', script, 'hid'], context)

class LogcatPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Debug"
    @property
    def icon(self): return "🐛"
    @property
    def description(self): return "Monitor de logs"

    def run(self, context):
        if not self._check_connection(context): return
        context.log("▶ Ejecutando Android Debug")
        script = self._get_script_path('android_logcat.sh')
        self._execute_subprocess(['bash', script], context)

class ScreenshotPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Snap"
    @property
    def icon(self): return "📸"
    @property
    def description(self): return "Captura de pantalla"

    def run(self, context):
        if not self._check_connection(context): return
        context.log("▶ Ejecutando Android Snap")
        script = self._get_script_path('android_screenshot.sh')
        
        def _thread_target():
            try:
                env = self.device_manager.get_env_for_scripts()
                result = subprocess.run(['bash', script], capture_output=True, timeout=10, env=env)
                if result.returncode == 0:
                    context.schedule_ui_update(lambda: context.log("✓ Captura guardada en el Escritorio"))
                else:
                    context.schedule_ui_update(lambda: context.log("✕ Error al capturar pantalla"))
            except Exception as e:
                context.schedule_ui_update(lambda: context.log(f"✕ Error: {str(e)}"))

        thread = threading.Thread(target=_thread_target, daemon=True)
        thread.start()

class RebootPlugin(BaseScriptPlugin):
    @property
    def name(self): return "Android Reset"
    @property
    def icon(self): return "🚑"
    @property
    def description(self): return "Reiniciar dispositivo"

    def run(self, context):
        # Reboot might not need a connected device if it's stuck? But script usually needs adb.
        # Original code didn't check connection explicitly for reboot but script likely fails if none.
        context.log("▶ Ejecutando Android Reset")
        script = self._get_script_path('android_reboot.sh')
        
        def _thread_target():
            try:
                env = self.device_manager.get_env_for_scripts()
                result = subprocess.run(['bash', script], capture_output=True, timeout=30, env=env)
                if result.returncode == 0:
                    context.schedule_ui_update(lambda: context.log("✓ Reinicio completado"))
                else:
                    context.schedule_ui_update(lambda: context.log("✕ Error al reiniciar"))
            except Exception as e:
                context.schedule_ui_update(lambda: context.log(f"✕ Error: {str(e)}"))

        thread = threading.Thread(target=_thread_target, daemon=True)
        thread.start()
