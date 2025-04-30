# pipeline.py
class SoccerAnalysisPipeline:
    """Orchestrates the complete data processing flow."""
    
    def __init__(self, config_path=None):
        """Initialize pipeline with optional configuration."""
        self.config = self._load_config(config_path) if config_path else self._default_config()
        self.loader = DartfishLoader()
        self.preprocessor = DataPreprocessor()
        self.event_classifier = EventClassifier(self.config)
        self.analyzers = self._initialize_analyzers()
        self.cache_manager = CacheManager(self.config.get('cache_settings', {}))
        
    def _initialize_analyzers(self):
        """Initialize all analysis components."""
        return {
            'momentum': MomentumAnalyzer(self.config.get('momentum_settings', {})),
            'pressing': PressingAnalyzer(self.config.get('pressing_settings', {})),
            'possession': PossessionAnalyzer(self.config.get('possession_settings', {})),
            'player': PlayerAnalyzer(self.config.get('player_settings', {})),
        }
        
    def process_match(self, first_half_path, second_half_path, cache_key=None):
        """Process a complete match through the entire pipeline."""
        # Check cache first if caching enabled
        if cache_key and self.cache_manager.has_cache(cache_key):
            return self.cache_manager.get_cache(cache_key)
            
        # Load and preprocess data
        raw_data = self.loader.load_match(first_half_path, second_half_path)
        preprocessed_data = self.preprocessor.preprocess(raw_data)
        
        # Classify events
        classified_events = self.event_classifier.classify(preprocessed_data)
        
        # Run all analyzers
        results = {}
        for name, analyzer in self.analyzers.items():
            results[name] = analyzer.analyze(classified_events)
        
        # Cache results if caching enabled
        if cache_key:
            self.cache_manager.cache(cache_key, results)
            
        return results