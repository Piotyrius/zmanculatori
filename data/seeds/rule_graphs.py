"""
Rule graphs seed data.

Creates rule graphs for each block type, linking to drafting schools.
"""
from typing import Dict, List


def get_rule_graphs() -> List[Dict[str, any]]:
    """Get all rule graph configurations for seeding."""
    return [
        {
            "name": "Bodice (No Darts) Rule Graph",
            "version": "1.0",
            "config_jsonb": {
                "id": "bodice-no-darts-rules",
                "version": "1.0",
                "nodes": [
                    {
                        "id": "compute_armhole_depth",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "chest / 4 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["armhole_depth"],
                    },
                    {
                        "id": "construct_back_point",
                        "type": "CONSTRUCT_POINT",
                        "inputs": ["armhole_depth"],
                        "params": {"x": 0, "y": 0},
                    },
                ],
            },
        },
        {
            "name": "Bodice (Waist Darts) Rule Graph",
            "version": "1.0",
            "config_jsonb": {
                "id": "bodice-waist-darts-rules",
                "version": "1.0",
                "nodes": [
                    {
                        "id": "compute_armhole_depth",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "chest / 4 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["armhole_depth"],
                    },
                    {
                        "id": "compute_dart_intake",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "(bust - waist) / 4",
                            "formula_type": "derived",
                        },
                        "outputs": ["dart_intake"],
                    },
                ],
            },
        },
        {
            "name": "Shirt Block Rule Graph",
            "version": "1.0",
            "config_jsonb": {
                "id": "shirt-block-rules",
                "version": "1.0",
                "nodes": [
                    {
                        "id": "compute_armhole_depth",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "chest / 4 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["armhole_depth"],
                    },
                ],
            },
        },
        {
            "name": "Skirt Block Rule Graph",
            "version": "1.0",
            "config_jsonb": {
                "id": "skirt-block-rules",
                "version": "1.0",
                "nodes": [
                    {
                        "id": "compute_skirt_width",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "hip / 2 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["skirt_width"],
                    },
                ],
            },
        },
        {
            "name": "Trouser Block Rule Graph",
            "version": "1.0",
            "config_jsonb": {
                "id": "trouser-block-rules",
                "version": "1.0",
                "nodes": [
                    {
                        "id": "compute_crotch_depth",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "hip / 4 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["crotch_depth"],
                    },
                ],
            },
        },
    ]

