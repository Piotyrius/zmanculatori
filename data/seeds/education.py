"""
Educational content seed data.

Includes descriptions for drafting schools, measurement logic explanations,
fit and ease guidance, and configuration warnings.
"""
from typing import Dict, List


def get_educational_content() -> List[Dict[str, any]]:
    """Get all educational content for seeding."""
    return [
        {
            "title": "Müller & Sohn Drafting System",
            "content_type": "drafting_school_description",
            "content": """
# Müller & Sohn Drafting System

The Müller & Sohn system is a German metric pattern cutting method known for its precision and systematic approach.

## Key Characteristics

- Uses metric measurements exclusively
- Emphasizes proportional relationships
- Suitable for both womenswear and menswear
- Well-documented and widely taught in European fashion schools

## Measurement Requirements

This system requires the following measurements:
- Bust/Chest
- Waist
- Hip
- Back length
- Shoulder width
- Body height

Optional measurements include bust point distance and height for more precise fitting.
            """,
            "language": "en",
            "priority": 1,
            "drafting_school_id": None,  # Will be linked during seeding
            "drafting_school_version": None,
            "metadata_jsonb": {},
        },
        {
            "title": "Understanding Measurement Categories",
            "content_type": "measurement_logic",
            "content": """
# Understanding Measurement Categories

Measurements are organized into categories to help you understand what's needed for different garment types.

## Core Girth Measurements (A)

These are the primary circumference measurements:
- **Bust/Chest**: The fullest part of the torso
- **Waist**: Natural waistline
- **Hip**: Widest part of the hips

## Vertical Measurements (B)

These measure length and depth:
- **Body Height**: Total height
- **Back Length**: From nape to waist
- **Front Length**: From shoulder to waist

## Width and Depth Measurements (C)

These measure horizontal dimensions:
- **Shoulder Width**: Across the back
- **Back Width**: Across shoulder blades
- **Armhole Depth**: Depth of armhole opening
            """,
            "language": "en",
            "priority": 2,
            "metadata_jsonb": {},
        },
        {
            "title": "Fit and Ease Guide",
            "content_type": "fit_guidance",
            "content": """
# Fit and Ease Guide

Understanding ease is crucial for creating well-fitting garments.

## Fit Profiles

- **Close Fit**: Minimal ease, body-hugging
- **Regular Fit**: Standard ease for comfort
- **Loose Fit**: Generous ease for movement
- **Oversized**: Significant ease for style

## Ease Categories

- **Wearing Ease**: Basic comfort allowance
- **Design Ease**: Style-specific additions
- **Functional Ease**: Movement and activity allowance
- **Production Ease**: Manufacturing tolerance

Ease must be applied parametrically, not destructively, so you can adjust it later.
            """,
            "language": "en",
            "priority": 3,
            "metadata_jsonb": {},
        },
        {
            "title": "Dart Operations",
            "content_type": "general",
            "content": """
# Dart Operations

Darts are used to shape fabric to fit the body's curves.

## Dart Types

- **Waist Darts**: Shape the waistline
- **Bust Darts**: Accommodate bust fullness
- **Shoulder Darts**: Shape the shoulder area
- **French Darts**: Diagonal darts from side seam

## Dart Operations

- **Rotate**: Move dart to different location
- **Split**: Divide into multiple darts
- **Eliminate**: Remove dart through design ease

All dart operations are reversible and rule-based.
            """,
            "language": "en",
            "priority": 4,
            "metadata_jsonb": {},
        },
        {
            "title": "Configuration Compatibility Warning",
            "content_type": "configuration_warning",
            "content": """
# Configuration Compatibility

⚠️ **Warning**: Not all drafting schools are compatible with all blocks.

Some combinations may produce unexpected results:
- Industrial systems may not work well with bespoke blocks
- Metric systems require metric measurements
- Some schools have specific block requirements

Always test your configuration before production use.
            """,
            "language": "en",
            "priority": 5,
            "metadata_jsonb": {},
        },
    ]

