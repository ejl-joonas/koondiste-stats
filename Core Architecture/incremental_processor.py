# incremental_processor.py
class IncrementalProcessor:
    """Supports incremental updates to analysis."""
    
    def update_analysis(self, match_id, new_events):
        """Update existing analysis with new events (e.g., from live tagging)."""
        # Retrieve existing analysis
        existing_analysis = self.cache_manager.get_cache(f"match:{match_id}")
        
        # Merge new events with existing events
        updated_events = self._merge_events(existing_analysis['events'], new_events)
        
        # Re-run affected portions of analysis
        updated_analysis = self._recompute_analysis(existing_analysis, updated_events)
        
        # Update cache
        self.cache_manager.cache(f"match:{match_id}", updated_analysis)
        
        return updated_analysis