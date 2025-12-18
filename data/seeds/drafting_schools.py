"""
Drafting schools seed data.

Includes all 5 categories of drafting schools with at least one example each.
"""
from typing import Dict, List

from engine.schools.models import DraftingSchoolCategory


def get_drafting_schools() -> List[Dict[str, any]]:
    """Get all drafting school configurations for seeding."""
    return [
        # 1. Metric Pattern Cutting (European)
        {
            "name": "Müller & Sohn",
            "version": "1.0",
            "config_jsonb": {
                "id": "muller-sohn",
                "name": "Müller & Sohn",
                "version": "1.0",
                "category": "metric_pattern_cutting",
                "description": "German metric pattern cutting system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                        "body_height",
                    ],
                    "optional": [
                        "bust_point_distance",
                        "bust_point_height",
                        "shoulder_slope",
                    ],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2",
                    "neck_width": "neck_circumference / 5",
                    "shoulder_slope": "back_length / 10",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                    "hip": {"wearing": 2, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        {
            "name": "ESMOD",
            "version": "1.0",
            "config_jsonb": {
                "id": "esmod",
                "name": "ESMOD",
                "version": "1.0",
                "category": "metric_pattern_cutting",
                "description": "French fashion school pattern cutting system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": ["bust_point_distance", "bust_point_height"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1.5",
                    "neck_width": "neck_circumference / 5.5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 3, "design": 0, "functional": 2},
                    "waist": {"wearing": 1.5, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "proportional",
                },
            },
            "is_active": True,
        },
        {
            "name": "Bunka (Japanese Hybrid)",
            "version": "1.0",
            "config_jsonb": {
                "id": "bunka",
                "name": "Bunka (Japanese Hybrid)",
                "version": "1.0",
                "category": "metric_pattern_cutting",
                "description": "Japanese hybrid metric system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                        "body_height",
                    ],
                    "optional": ["bust_point_distance", "bust_point_height"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1",
                    "neck_width": "neck_circumference / 6",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 3, "design": 0, "functional": 1},
                    "waist": {"wearing": 1, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "fixed",
                    "dart_distribution": "proportional",
                },
            },
            "is_active": True,
        },
        {
            "name": "Italian Industrial System",
            "version": "1.0",
            "config_jsonb": {
                "id": "italian-industrial",
                "name": "Italian Industrial System",
                "version": "1.0",
                "category": "metric_pattern_cutting",
                "description": "Italian industrial pattern cutting system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2.5",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        # 2. Anglo-American Systems
        {
            "name": "Winifred Aldrich",
            "version": "1.0",
            "config_jsonb": {
                "id": "winifred-aldrich",
                "name": "Winifred Aldrich",
                "version": "1.0",
                "category": "anglo_american",
                "description": "British pattern cutting system by Winifred Aldrich",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": ["bust_point_distance", "bust_point_height"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 5, "design": 0, "functional": 2},
                    "waist": {"wearing": 2.5, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        {
            "name": "Helen Joseph-Armstrong",
            "version": "1.0",
            "config_jsonb": {
                "id": "helen-joseph-armstrong",
                "name": "Helen Joseph-Armstrong",
                "version": "1.0",
                "category": "anglo_american",
                "description": "American pattern making system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": ["bust_point_distance", "bust_point_height"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1.5",
                    "neck_width": "neck_circumference / 5.5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 5, "design": 0, "functional": 2},
                    "waist": {"wearing": 2.5, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "proportional",
                },
            },
            "is_active": True,
        },
        {
            "name": "Natalie Bray",
            "version": "1.0",
            "config_jsonb": {
                "id": "natalie-bray",
                "name": "Natalie Bray",
                "version": "1.0",
                "category": "anglo_american",
                "description": "British tailoring pattern system",
                "measurement_requirements": {
                    "required": [
                        "chest",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "chest": {"wearing": 6, "design": 0, "functional": 3},
                    "waist": {"wearing": 3, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        {
            "name": "Traditional British Tailoring",
            "version": "1.0",
            "config_jsonb": {
                "id": "traditional-british-tailoring",
                "name": "Traditional British Tailoring",
                "version": "1.0",
                "category": "anglo_american",
                "description": "Classic British tailoring system",
                "measurement_requirements": {
                    "required": [
                        "chest",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2.5",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "chest": {"wearing": 7, "design": 0, "functional": 3},
                    "waist": {"wearing": 3, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        # 3. Flat Pattern Industrial
        {
            "name": "Ready-to-Wear Block System",
            "version": "1.0",
            "config_jsonb": {
                "id": "rtw-block-system",
                "name": "Ready-to-Wear Block System",
                "version": "1.0",
                "category": "flat_pattern_industrial",
                "description": "Industrial ready-to-wear block system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2, "production": 1},
                    "waist": {"wearing": 2, "design": 0, "functional": 0, "production": 0.5},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "standardized",
                    "dart_distribution": "standardized",
                },
            },
            "is_active": True,
        },
        {
            "name": "Size-Chart Driven Drafting",
            "version": "1.0",
            "config_jsonb": {
                "id": "size-chart-driven",
                "name": "Size-Chart Driven Drafting",
                "version": "1.0",
                "category": "flat_pattern_industrial",
                "description": "Drafting based on standard size charts",
                "measurement_requirements": {
                    "required": ["bust", "waist", "hip"],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2, "production": 1},
                    "waist": {"wearing": 2, "design": 0, "functional": 0, "production": 0.5},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "standardized",
                    "dart_distribution": "standardized",
                },
            },
            "is_active": True,
        },
        {
            "name": "Production Grading System",
            "version": "1.0",
            "config_jsonb": {
                "id": "production-grading",
                "name": "Production Grading System",
                "version": "1.0",
                "category": "flat_pattern_industrial",
                "description": "Industrial production grading system",
                "measurement_requirements": {
                    "required": ["bust", "waist", "hip"],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 1",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2, "production": 1},
                    "waist": {"wearing": 2, "design": 0, "functional": 0, "production": 0.5},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "standardized",
                    "dart_distribution": "standardized",
                },
            },
            "is_active": True,
        },
        # 4. Tailoring-Based Systems
        {
            "name": "Bespoke Menswear Drafting",
            "version": "1.0",
            "config_jsonb": {
                "id": "bespoke-menswear",
                "name": "Bespoke Menswear Drafting",
                "version": "1.0",
                "category": "tailoring_based",
                "description": "Bespoke menswear pattern drafting system",
                "measurement_requirements": {
                    "required": [
                        "chest",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                        "arm_length",
                    ],
                    "optional": ["shoulder_slope", "neck_depth"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2.5",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "chest": {"wearing": 8, "design": 0, "functional": 4},
                    "waist": {"wearing": 3, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "custom",
                    "dart_distribution": "custom",
                },
            },
            "is_active": True,
        },
        {
            "name": "Structured Jackets and Coats",
            "version": "1.0",
            "config_jsonb": {
                "id": "structured-jackets",
                "name": "Structured Jackets and Coats",
                "version": "1.0",
                "category": "tailoring_based",
                "description": "Tailoring system for structured outerwear",
                "measurement_requirements": {
                    "required": [
                        "chest",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": ["arm_length"],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 3",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "chest": {"wearing": 10, "design": 0, "functional": 5},
                    "waist": {"wearing": 4, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        {
            "name": "Classic Tailoring Proportions",
            "version": "1.0",
            "config_jsonb": {
                "id": "classic-tailoring",
                "name": "Classic Tailoring Proportions",
                "version": "1.0",
                "category": "tailoring_based",
                "description": "Classic tailoring proportion system",
                "measurement_requirements": {
                    "required": [
                        "chest",
                        "waist",
                        "hip",
                        "back_length",
                        "front_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2.5",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "chest": {"wearing": 8, "design": 0, "functional": 4},
                    "waist": {"wearing": 3, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        # 5. Educational / Hybrid Systems
        {
            "name": "School-Agnostic Proportional Drafting",
            "version": "1.0",
            "config_jsonb": {
                "id": "school-agnostic",
                "name": "School-Agnostic Proportional Drafting",
                "version": "1.0",
                "category": "educational_hybrid",
                "description": "Generic proportional drafting system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "proportional",
                    "dart_distribution": "equal",
                },
            },
            "is_active": True,
        },
        {
            "name": "Simplified Teaching Blocks",
            "version": "1.0",
            "config_jsonb": {
                "id": "simplified-teaching",
                "name": "Simplified Teaching Blocks",
                "version": "1.0",
                "category": "educational_hybrid",
                "description": "Simplified blocks for teaching purposes",
                "measurement_requirements": {
                    "required": ["bust", "waist", "hip", "back_length"],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "simplified",
                    "dart_distribution": "simplified",
                },
            },
            "is_active": True,
        },
        {
            "name": "Experimental Parametric System",
            "version": "1.0",
            "config_jsonb": {
                "id": "experimental-parametric",
                "name": "Experimental Parametric System",
                "version": "1.0",
                "category": "educational_hybrid",
                "description": "Experimental parametric drafting system",
                "measurement_requirements": {
                    "required": [
                        "bust",
                        "waist",
                        "hip",
                        "back_length",
                        "shoulder_width",
                    ],
                    "optional": [],
                },
                "proportional_logic": {
                    "armhole_depth": "chest / 4 + 2",
                    "neck_width": "neck_circumference / 5",
                },
                "ease_philosophy": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                },
                "drafting_conventions": {
                    "shoulder_slope_method": "parametric",
                    "dart_distribution": "parametric",
                },
            },
            "is_active": True,
        },
    ]





