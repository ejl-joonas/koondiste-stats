# errors.py
class DataValidationError(Exception):
    """Raised when data doesn't meet expected format."""
    pass

class AnalysisError(Exception):
    """Raised when analysis can't be completed."""
    pass

# logging_config.py
def setup_logging(log_level, log_file=None):
    """Configure logging for the application."""