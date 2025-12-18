"""
Base block library seed data.

Includes all block types as defined in the domain specification.
"""
from typing import Dict, List


def get_blocks() -> List[Dict[str, any]]:
    """Get all block configurations for seeding."""
    return [
        # Upper Body Blocks
        {
            "name": "Bodice (No Darts)",
            "version": "1.0",
            "config_jsonb": {
                "id": "bodice-no-darts",
                "block_type": "bodice",
                "dart_configuration": "none",
                "drafting_school_id": None,  # Can be used with any school
                "drafting_school_version": None,
                "rule_graph_id": "bodice-no-darts-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Bodice (Waist Darts)",
            "version": "1.0",
            "config_jsonb": {
                "id": "bodice-waist-darts",
                "block_type": "bodice",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "bodice-waist-darts-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Shirt Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "shirt-block",
                "block_type": "shirt",
                "dart_configuration": "none",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "shirt-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Blouse Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "blouse-block",
                "block_type": "blouse",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "blouse-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Jacket Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "jacket-block",
                "block_type": "jacket",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "jacket-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Coat Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "coat-block",
                "block_type": "coat",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "coat-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        # Lower Body Blocks
        {
            "name": "Skirt Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "skirt-block",
                "block_type": "skirt",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "skirt-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Trouser Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "trouser-block",
                "block_type": "trouser",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "trouser-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Pants Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "pants-block",
                "block_type": "pants",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "pants-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Shorts Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "shorts-block",
                "block_type": "shorts",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "shorts-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        # Sleeve Blocks
        {
            "name": "One-Piece Sleeve",
            "version": "1.0",
            "config_jsonb": {
                "id": "one-piece-sleeve",
                "block_type": "sleeve",
                "sleeve_type": "one-piece",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "one-piece-sleeve-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Two-Piece Sleeve",
            "version": "1.0",
            "config_jsonb": {
                "id": "two-piece-sleeve",
                "block_type": "sleeve",
                "sleeve_type": "two-piece",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "two-piece-sleeve-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Raglan Sleeve",
            "version": "1.0",
            "config_jsonb": {
                "id": "raglan-sleeve",
                "block_type": "sleeve",
                "sleeve_type": "raglan",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "raglan-sleeve-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Kimono Sleeve",
            "version": "1.0",
            "config_jsonb": {
                "id": "kimono-sleeve",
                "block_type": "sleeve",
                "sleeve_type": "kimono",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "kimono-sleeve-rules",
                "rule_graph_version": "1.0",
            },
        },
        # Specialized Blocks
        {
            "name": "Dress Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "dress-block",
                "block_type": "dress",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "dress-block-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Corsetry Base",
            "version": "1.0",
            "config_jsonb": {
                "id": "corsetry-base",
                "block_type": "corsetry",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "corsetry-base-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Outerwear Base",
            "version": "1.0",
            "config_jsonb": {
                "id": "outerwear-base",
                "block_type": "outerwear",
                "dart_configuration": "waist",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "outerwear-base-rules",
                "rule_graph_version": "1.0",
            },
        },
        {
            "name": "Childrenswear Block",
            "version": "1.0",
            "config_jsonb": {
                "id": "childrenswear-block",
                "block_type": "childrenswear",
                "dart_configuration": "none",
                "drafting_school_id": None,
                "drafting_school_version": None,
                "rule_graph_id": "childrenswear-block-rules",
                "rule_graph_version": "1.0",
            },
        },
    ]



