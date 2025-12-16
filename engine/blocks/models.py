from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class BlockDefinition:
    id: str
    version: str
    block_type: str
    drafting_school_id: str
    drafting_school_version: str
    rule_graph_id: str
    rule_graph_version: str
    default_transform_pipeline_id: Optional[str] = None
    seam_allowance_profile_id: Optional[str] = None





