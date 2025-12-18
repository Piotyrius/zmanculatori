from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ContentType(str, Enum):
    """Types of educational content."""
    DRAFTING_SCHOOL_DESCRIPTION = "drafting_school_description"
    MEASUREMENT_LOGIC = "measurement_logic"
    FIT_GUIDANCE = "fit_guidance"
    EASE_GUIDANCE = "ease_guidance"
    CONFIGURATION_WARNING = "configuration_warning"
    GENERAL = "general"


@dataclass(slots=True)
class EducationalContent:
    """
    Educational content for designers.
    
    This content must be optional and non-blocking.
    """
    id: str
    title: str
    content_type: ContentType
    content: str  # Markdown content
    
    # Links to related resources
    drafting_school_id: Optional[str] = None
    drafting_school_version: Optional[str] = None
    block_id: Optional[str] = None
    block_version: Optional[str] = None
    measurement_name: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, any] = field(default_factory=dict)
    
    # Language support (optional)
    language: str = "en"
    
    # Priority/ordering
    priority: int = 0  # Lower numbers shown first



