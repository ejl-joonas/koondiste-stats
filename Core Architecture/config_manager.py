# config_manager.py
class ConfigManager:
    """Manages all configuration aspects of the analysis system."""
    
    def __init__(self, base_config_path=None):
        """Initialize with optional path to base configuration."""
        self.base_config_path = base_config_path or "config/base_config.yaml"
        self.user_config_path = "config/user_config.yaml"
        
        # Load configurations in priority order (later ones override earlier ones)
        self.config = {}
        self._load_builtin_defaults()
        self._load_yaml_config(self.base_config_path)
        
        # Only load user config if it exists
        if os.path.exists(self.user_config_path):
            self._load_yaml_config(self.user_config_path)
            
    def _load_builtin_defaults(self):
        """Load built-in default configuration."""
        self.config = {
            "analysis": {
                "intervals": {"minutes": 5},
                "momentum": {"default_decay": 0.2}
            },
            "display": {
                "language": "en",
                "decimal_places": 2
            }
        }
        
    def _load_yaml_config(self, config_path):
        """Load and merge YAML configuration."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)
                self._deep_update(self.config, yaml_config)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {str(e)}")
            
    def _deep_update(self, target, source):
        """Deep update target dict with source without overwriting entire nested dicts."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
                
    def get(self, key_path, default=None):
        """Get configuration value by dot-notation path."""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if key not in value:
                return default
            value = value[key]
        return value
        
    def update_runtime(self, key_path, value):
        """Update configuration at runtime (doesn't persist)."""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        
    def save_user_config(self):
        """Save current configuration as user configuration."""
        os.makedirs(os.path.dirname(self.user_config_path), exist_ok=True)
        with open(self.user_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)