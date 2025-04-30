# batch_processor.py
class BatchProcessor:
    """Processes multiple matches in batch."""
    
    def process_matches(self, match_paths_list):
        """Process a batch of matches with shared configuration."""
        results = {}
        for match_id, paths in match_paths_list.items():
            results[match_id] = self.pipeline.process_match(
                paths['first_half'], 
                paths['second_half'],
                cache_key=f"match:{match_id}"
            )
        return results
    
    def process_tournament(self, tournament_path):
        """Process an entire tournament folder structure."""
        # Automatically discover match files within tournament structure
        match_paths = self._discover_matches(tournament_path)
        return self.process_matches(match_paths)