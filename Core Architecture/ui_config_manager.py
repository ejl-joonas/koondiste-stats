# ui_config_manager.py
class UIConfigManager:
    """Manages UI configuration with live updates."""
    
    def __init__(self, config_manager):
        """Initialize with configuration manager."""
        self.config_manager = config_manager
        self.ui_config = self.config_manager.get("ui", {})
        self.observers = {}
        
    def register_observer(self, config_path, callback):
        """Register a callback for configuration changes."""
        if config_path not in self.observers:
            self.observers[config_path] = []
        self.observers[config_path].append(callback)
        
    def update_config(self, config_path, value):
        """Update configuration and notify observers."""
        # Update config
        self.config_manager.update_runtime(config_path, value)
        
        # Notify observers
        if config_path in self.observers:
            for callback in self.observers[config_path]:
                try:
                    callback(value)
                except Exception as e:
                    logger.error(f"Error in config observer callback: {str(e)}")
                    
        # Check if this is a parent path of other observers
        for observer_path in self.observers:
            if observer_path.startswith(config_path + "."):
                # This is a child config, get its updated value
                sub_path = observer_path[len(config_path)+1:]
                new_parent_value = self.config_manager.get(config_path, {})
                
                # Navigate to the specific child value
                sub_keys = sub_path.split(".")
                current = new_parent_value
                for key in sub_keys:
                    if key not in current:
                        current = None
                        break
                    current = current[key]
                
                # Notify observers of child path
                if current is not None:
                    for callback in self.observers[observer_path]:
                        try:
                            callback(current)
                        except Exception as e:
                            logger.error(f"Error in config observer callback: {str(e)}")