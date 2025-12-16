from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(slots=True)
class ExportOptions:
    format: str = "svg"
    debug: bool = False
    dpi: int = 96
    scale: float = 1.0


@dataclass(slots=True)
class ExportBundle:
    """
    Result of an export operation.

    The bytes are typically SVG/DXF/PDF contents; metadata may include
    dimensions, units, and any debug flags used.
    """

    content: bytes
    mime_type: str
    metadata: Dict[str, object]



