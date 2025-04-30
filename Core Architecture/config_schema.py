# config_schema.py
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union, Any

class ZoneConfig(BaseModel):
    """Configuration for a pitch zone."""
    start_y: float = Field(..., ge=0, le=100)
    end_y: float = Field(..., ge=0, le=100)
    description: Optional[str] = None
    
    @validator('end_y')
    def end_must_be_greater_than_start(cls, v, values):
        if 'start_y' in values and v <= values['start_y']:
            raise ValueError('end_y must be greater than start_y')
        return v

class MomentumConfig(BaseModel):
    """Configuration for momentum analysis."""
    point_values: Dict[str, float]
    decay: Dict[str, float] = {"factor": 0.2, "window": 2}
    active_model: str = "default"

class ZonesConfig(BaseModel):
    """Configuration for all pitch zones."""
    pressing: Dict[str, ZoneConfig]
    progression: Dict[str, ZoneConfig]

class AnalysisConfig(BaseModel):
    """Configuration for analysis parameters."""
    intervals: Dict[str, int] = {"minutes": 5}
    momentum: MomentumConfig
    zones: ZonesConfig

class TranslationEntry(BaseModel):
    """Entry for a taxonomy term with translations."""
    code: str
    en: str
    et: Optional[str] = None

class TaxonomiesConfig(BaseModel):
    """Configuration for all taxonomies."""
    possession: Dict[str, TranslationEntry]
    outcomes: Dict[str, TranslationEntry]
    # Add other taxonomies as needed

class DisplayConfig(BaseModel):
    """Configuration for display settings."""
    language: str = "en"
    decimal_places: int = 2
    charts: Dict[str, Any] = {}

class CacheConfig(BaseModel):
    """Configuration for caching."""
    enabled: bool = True
    ttl_seconds: int = 3600
    max_entries: int = 100

class ProcessingConfig(BaseModel):
    """Configuration for data processing."""
    cache: CacheConfig

class CompleteConfig(BaseModel):
    """Complete configuration schema."""
    analysis: AnalysisConfig
    taxonomies: TaxonomiesConfig
    display: DisplayConfig
    processing: ProcessingConfig