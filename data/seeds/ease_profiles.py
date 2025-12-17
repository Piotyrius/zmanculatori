"""
Ease profiles seed data.

Creates ease profiles for each fit type, linking to drafting schools where applicable.
"""
from typing import Dict, List


def get_ease_profiles() -> List[Dict[str, any]]:
    """Get all ease profile configurations for seeding."""
    return [
        {
            "name": "Close Fit",
            "version": "1.0",
            "config_jsonb": {
                "id": "close-fit",
                "name": "Close Fit",
                "version": "1.0",
                "fit_profile": "close",
                "ease_values": {
                    "bust": {"wearing": 2, "design": 0, "functional": 1},
                    "waist": {"wearing": 1, "design": 0, "functional": 0},
                    "hip": {"wearing": 1, "design": 0, "functional": 0},
                },
            },
        },
        {
            "name": "Regular Fit",
            "version": "1.0",
            "config_jsonb": {
                "id": "regular-fit",
                "name": "Regular Fit",
                "version": "1.0",
                "fit_profile": "regular",
                "ease_values": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                    "hip": {"wearing": 2, "design": 0, "functional": 0},
                },
            },
        },
        {
            "name": "Loose Fit",
            "version": "1.0",
            "config_jsonb": {
                "id": "loose-fit",
                "name": "Loose Fit",
                "version": "1.0",
                "fit_profile": "loose",
                "ease_values": {
                    "bust": {"wearing": 6, "design": 0, "functional": 3},
                    "waist": {"wearing": 4, "design": 0, "functional": 0},
                    "hip": {"wearing": 4, "design": 0, "functional": 0},
                },
            },
        },
        {
            "name": "Oversized Fit",
            "version": "1.0",
            "config_jsonb": {
                "id": "oversized-fit",
                "name": "Oversized Fit",
                "version": "1.0",
                "fit_profile": "oversized",
                "ease_values": {
                    "bust": {"wearing": 10, "design": 5, "functional": 5},
                    "waist": {"wearing": 8, "design": 4, "functional": 0},
                    "hip": {"wearing": 8, "design": 4, "functional": 0},
                },
            },
        },
        {
            "name": "Müller & Sohn Default Ease",
            "version": "1.0",
            "config_jsonb": {
                "id": "muller-sohn-ease",
                "name": "Müller & Sohn Default Ease",
                "version": "1.0",
                "fit_profile": "regular",
                "drafting_school_id": "muller-sohn",
                "drafting_school_version": "1.0",
                "ease_values": {
                    "bust": {"wearing": 4, "design": 0, "functional": 2},
                    "waist": {"wearing": 2, "design": 0, "functional": 0},
                    "hip": {"wearing": 2, "design": 0, "functional": 0},
                },
            },
        },
    ]

