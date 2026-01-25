
import os
import json

class ConfigManager:
    _instance = None
    
    DEFAULT_CONFIG = {
        "scrcpy_path": "scrcpy",
        "recordings_path": os.path.expanduser("~/Videos/Android_Recordings"),
        "mirror_args": "-m1024 --max-fps=30 -b4M -S --no-audio --window-title 'Android Mirror' --show-touches",
        "theme": "dark"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config_file = os.path.expanduser("~/.config/miru/config.json")
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        self.config = self.DEFAULT_CONFIG.copy()
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
