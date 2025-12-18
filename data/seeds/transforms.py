"""
Transform pipelines seed data.

Includes dart operations, style transformations, grading, and seam allowance pipelines.
"""
from typing import Dict, List


def get_transform_pipelines() -> List[Dict[str, any]]:
    """Get all transform pipeline configurations for seeding."""
    return [
        {
            "name": "Waist Dart Rotation",
            "version": "1.0",
            "config_jsonb": {
                "id": "waist-dart-rotation",
                "version": "1.0",
                "steps": [
                    {
                        "id": "rotate_waist_dart",
                        "type": "DART",
                        "params": {
                            "dart_type": "waist",
                            "operation": "rotate",
                            "target_location": "shoulder",
                        },
                    },
                ],
            },
        },
        {
            "name": "Bust Dart Split",
            "version": "1.0",
            "config_jsonb": {
                "id": "bust-dart-split",
                "version": "1.0",
                "steps": [
                    {
                        "id": "split_bust_dart",
                        "type": "DART",
                        "params": {
                            "dart_type": "bust",
                            "operation": "split",
                            "split_count": 2,
                        },
                    },
                ],
            },
        },
        {
            "name": "Add Flare",
            "version": "1.0",
            "config_jsonb": {
                "id": "add-flare",
                "version": "1.0",
                "steps": [
                    {
                        "id": "add_flare",
                        "type": "STYLE",
                        "params": {
                            "transformation": "flare",
                            "amount": 5.0,
                        },
                    },
                ],
            },
        },
        {
            "name": "Lengthen Garment",
            "version": "1.0",
            "config_jsonb": {
                "id": "lengthen-garment",
                "version": "1.0",
                "steps": [
                    {
                        "id": "lengthen",
                        "type": "STYLE",
                        "params": {
                            "transformation": "lengthen",
                            "amount": 50.0,
                        },
                    },
                ],
            },
        },
        {
            "name": "Add Seam Allowance",
            "version": "1.0",
            "config_jsonb": {
                "id": "add-seam-allowance",
                "version": "1.0",
                "steps": [
                    {
                        "id": "seam_allowance",
                        "type": "SEAM_ALLOWANCE",
                        "params": {
                            "default": 10.0,
                            "overrides": {},
                        },
                    },
                ],
            },
        },
        {
            "name": "Grade to Size Range",
            "version": "1.0",
            "config_jsonb": {
                "id": "grade-size-range",
                "version": "1.0",
                "steps": [
                    {
                        "id": "grade",
                        "type": "GRADING",
                        "params": {
                            "size_range_id": "standard-sizes",
                            "target_size": "L",
                        },
                    },
                ],
            },
        },
    ]


