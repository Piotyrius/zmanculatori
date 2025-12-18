"""
Measurement system seed data.

Defines all measurement categories (A-F) and validation schemas.
"""
from typing import Dict, List

# Measurement categories as defined in the domain specification
MEASUREMENT_CATEGORIES: Dict[str, Dict[str, any]] = {
    # A. Core Girth Measurements
    "bust": {
        "category": "core_girth",
        "description": "Bust circumference at fullest point",
        "is_required": True,
    },
    "chest": {
        "category": "core_girth",
        "description": "Chest circumference at fullest point",
        "is_required": True,
    },
    "waist": {
        "category": "core_girth",
        "description": "Waist circumference at natural waist",
        "is_required": True,
    },
    "hip": {
        "category": "core_girth",
        "description": "Hip circumference at fullest point",
        "is_required": True,
    },
    "high_hip": {
        "category": "core_girth",
        "description": "High hip circumference",
        "is_required": False,
    },
    "underbust": {
        "category": "core_girth",
        "description": "Underbust circumference",
        "is_required": False,
    },
    "neck_circumference": {
        "category": "core_girth",
        "description": "Neck circumference at base",
        "is_required": True,
    },
    # B. Vertical Measurements
    "body_height": {
        "category": "vertical",
        "description": "Total body height",
        "is_required": True,
    },
    "back_length": {
        "category": "vertical",
        "description": "Back length from nape to waist",
        "is_required": True,
    },
    "front_length": {
        "category": "vertical",
        "description": "Front length from shoulder to waist",
        "is_required": True,
    },
    "waist_to_hip": {
        "category": "vertical",
        "description": "Vertical distance from waist to hip",
        "is_required": False,
    },
    "shoulder_to_waist": {
        "category": "vertical",
        "description": "Vertical distance from shoulder to waist",
        "is_required": False,
    },
    "rise": {
        "category": "vertical",
        "description": "Crotch depth (rise)",
        "is_required": False,
    },
    "crotch_depth": {
        "category": "vertical",
        "description": "Crotch depth measurement",
        "is_required": False,
    },
    # C. Width and Depth Measurements
    "shoulder_width": {
        "category": "width_depth",
        "description": "Shoulder width across back",
        "is_required": True,
    },
    "back_width": {
        "category": "width_depth",
        "description": "Back width across shoulder blades",
        "is_required": False,
    },
    "front_width": {
        "category": "width_depth",
        "description": "Front width across chest",
        "is_required": False,
    },
    "armhole_depth": {
        "category": "width_depth",
        "description": "Armhole depth",
        "is_required": False,
    },
    "chest_depth": {
        "category": "width_depth",
        "description": "Chest depth measurement",
        "is_required": False,
    },
    # D. Sleeve Measurements
    "arm_length": {
        "category": "sleeve",
        "description": "Arm length from shoulder to wrist",
        "is_required": False,
    },
    "upper_arm_circumference": {
        "category": "sleeve",
        "description": "Upper arm circumference",
        "is_required": False,
    },
    "elbow_circumference": {
        "category": "sleeve",
        "description": "Elbow circumference",
        "is_required": False,
    },
    "wrist_circumference": {
        "category": "sleeve",
        "description": "Wrist circumference",
        "is_required": False,
    },
    "armhole_circumference": {
        "category": "sleeve",
        "description": "Armhole circumference",
        "is_required": False,
    },
    # E. Leg Measurements
    "inseam": {
        "category": "leg",
        "description": "Inside leg length",
        "is_required": False,
    },
    "outseam": {
        "category": "leg",
        "description": "Outside leg length",
        "is_required": False,
    },
    "thigh": {
        "category": "leg",
        "description": "Thigh circumference",
        "is_required": False,
    },
    "knee": {
        "category": "leg",
        "description": "Knee circumference",
        "is_required": False,
    },
    "calf": {
        "category": "leg",
        "description": "Calf circumference",
        "is_required": False,
    },
    "ankle": {
        "category": "leg",
        "description": "Ankle circumference",
        "is_required": False,
    },
    # F. Optional / Advanced
    "bust_point_distance": {
        "category": "optional",
        "description": "Distance between bust points",
        "is_required": False,
    },
    "bust_point_height": {
        "category": "optional",
        "description": "Height of bust point from shoulder",
        "is_required": False,
    },
    "shoulder_slope": {
        "category": "optional",
        "description": "Shoulder slope angle",
        "is_required": False,
    },
    "neck_depth": {
        "category": "optional",
        "description": "Neck depth measurement",
        "is_required": False,
    },
}


def get_measurement_categories() -> List[Dict[str, any]]:
    """Get all measurement category definitions for seeding."""
    return [
        {
            "name": name,
            "category": info["category"],
            "description": info["description"],
            "is_required": info["is_required"],
            "metadata_jsonb": {},
        }
        for name, info in MEASUREMENT_CATEGORIES.items()
    ]


def get_example_measurement_profiles() -> List[Dict[str, any]]:
    """Get example measurement profiles for each category."""
    return [
        {
            "name": "Standard Womenswear Size 10",
            "category": "womenswear",
            "unit": "mm",
            "values": {
                "bust": 920,
                "waist": 760,
                "hip": 1000,
                "body_height": 1650,
                "back_length": 420,
                "front_length": 450,
                "shoulder_width": 380,
                "neck_circumference": 360,
            },
        },
        {
            "name": "Standard Menswear Size M",
            "category": "menswear",
            "unit": "mm",
            "values": {
                "chest": 1000,
                "waist": 860,
                "hip": 980,
                "body_height": 1750,
                "back_length": 480,
                "front_length": 500,
                "shoulder_width": 420,
                "neck_circumference": 400,
            },
        },
    ]





