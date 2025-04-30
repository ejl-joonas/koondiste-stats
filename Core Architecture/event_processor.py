# event_processor.py
class EventClassifier:
    """Classifies raw events into tactical categories."""
    
    def classify_possession_events(self, events):
        """Classify events by possession type (AA, DD, AD, DA)."""
    
    def classify_pressing_events(self, events):
        """Identify and categorize pressing events (HIGH, MID, LOW)."""
    
    def classify_zone_progressions(self, events):
        """Track zone progressions (S1, S2, S3)."""
        
    def identify_set_pieces(self, events):
        """Extract set piece events and their outcomes."""