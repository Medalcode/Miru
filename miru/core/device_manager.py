
import subprocess
import re
import os

class DeviceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DeviceManager, cls).__new__(cls)
        return cls._instance

    def get_device_selector(self):
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
                                return f"-s {part}"
                        
                        # Si no hay USB path, intentar transport_id
                        for part in parts:
                            if part.startswith('transport_id:'):
                                tid = part.split(':')[1]
                                return f"-t {tid}"
                        
                        # Fallback al serial
                        return f"-s {serial}"
            
            return None
        except Exception as e:
            print(f"Error getting device serial: {e}")
            return None

    def get_device_info(self, selector):
        """Obtiene información del dispositivo"""
        if not selector:
            return None
        
        # Split device selector into flag and value
        selector_parts = selector.split()  # e.g., ['-t', '1'] or ['-s', 'SERIAL']
        
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

    def get_env_for_scripts(self):
        """Genera el entorno con las variables necesarias para los scripts"""
        env = os.environ.copy()
        selector = self.get_device_selector()
        if selector:
            env['MIRU_ADB_DEVICE'] = selector
            if selector.startswith('-s '):
                env['ANDROID_SERIAL'] = selector[3:]
        return env
