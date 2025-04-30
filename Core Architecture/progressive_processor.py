# progressive_processor.py
class ProgressiveProcessor:
    """Processes data progressively, allowing for early insights."""
    
    def process_progressively(self, match_paths, callback=None):
        """Process match data with progressive updates."""
        # First provide quick summary stats
        raw_data = self.loader.load_match_quick(match_paths['first_half'], match_paths['second_half'])
        summary = self._generate_quick_summary(raw_data)
        if callback:
            callback('summary', summary)
        
        # Then do full preprocessing
        preprocessed_data = self.preprocessor.preprocess(raw_data)
        if callback:
            callback('preprocessed', preprocessed_data)
        
        # Calculate basic stats
        basic_stats = self._calculate_basic_stats(preprocessed_data)
        if callback:
            callback('basic_stats', basic_stats)
        
        # Run complete analysis
        full_results = self._run_full_analysis(preprocessed_data)
        if callback:
            callback('complete', full_results)
        
        return full_results