# scoring_model.py
class ScoringModelManager:
    """Manages scoring models with version control and validation."""
    
    def __init__(self, config_manager):
        """Initialize with configuration manager."""
        self.config_manager = config_manager
        self.models_path = "config/scoring_models"
        
    def get_current_model(self):
        """Get currently active scoring model."""
        model_name = self.config_manager.get("analysis.momentum.active_model", "default")
        return self.load_model(model_name)
        
    def load_model(self, model_name):
        """Load a specific scoring model."""
        model_path = os.path.join(self.models_path, f"{model_name}.yaml")
        try:
            with open(model_path, 'r', encoding='utf-8') as f:
                model = yaml.safe_load(f)
                self._validate_model(model)
                return model
        except FileNotFoundError:
            logger.warning(f"Scoring model {model_name} not found, using defaults")
            return self._default_model()
        
    def _validate_model(self, model):
        """Validate scoring model structure and values."""
        # Check required sections
        required_sections = ["metadata", "point_values", "multipliers"]
        for section in required_sections:
            if section not in model:
                raise ValueError(f"Scoring model missing required section: {section}")
        
        # Validate point values are numeric
        for key, value in model["point_values"].items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"Point value for '{key}' must be numeric, got {type(value)}")
        
    def _default_model(self):
        """Provide default scoring model."""
        return {
            "metadata": {
                "name": "default",
                "description": "Default scoring model",
                "version": "1.0",
                "created": "2025-04-28"
            },
            "point_values": {
                "SHOTGOAL": 20.0,
                "SHOTON": 4.0,
                "SHOTBLOCK": 3.0,
                "SHOTOFF": 2.0,
                "ENTRY": 1.0,
                # ...etc
            },
            "multipliers": {
                "zone": {
                    "S1": 0.8,
                    "S2": 1.0,
                    "S3": 1.2
                },
                "pressing": {
                    "HIGHPRESS": 1.5,
                    "MIDPRESS": 1.0,
                    "LOWPRESS": 0.7
                }
            }
        }
        
    def save_model(self, model_name, model_data):
        """Save scoring model to file."""
        self._validate_model(model_data)
        
        # Ensure models directory exists
        os.makedirs(self.models_path, exist_ok=True)
        
        # Save the model
        model_path = os.path.join(self.models_path, f"{model_name}.yaml")
        with open(model_path, 'w', encoding='utf-8') as f:
            yaml.dump(model_data, f, default_flow_style=False, allow_unicode=True)
        
        return True
        
    def list_available_models(self):
        """List all available scoring models."""
        models = []
        if os.path.exists(self.models_path):
            for file in os.listdir(self.models_path):
                if file.endswith(".yaml"):
                    model_name = file[:-5]  # Remove .yaml extension
                    models.append(model_name)
        return models