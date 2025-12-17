"""
Grading calculator for pattern sizing.

Implements grading logic with support for proportional and linear grading,
and school-specific grading tables.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from .models import GradingTable, GradeRule, GradingMethod, SizeRange


def calculate_graded_measurements(
    base_measurements: Dict[str, float],
    grading_table: GradingTable,
    size_offset: int,
) -> Dict[str, float]:
    """
    Calculate graded measurements for a given size offset.
    
    Args:
        base_measurements: Base size measurements
        grading_table: Grading table to apply
        size_offset: Number of sizes from base (positive = larger, negative = smaller)
    
    Returns:
        Dict of graded measurement values
    """
    graded = {}
    for measurement_name, base_value in base_measurements.items():
        graded_value = grading_table.calculate_graded_value(
            measurement_name, base_value, size_offset
        )
        graded[measurement_name] = graded_value
    return graded


def apply_grading_to_pattern(
    pattern_geometry: any,  # PatternGeometry
    grading_table: GradingTable,
    size_offset: int,
) -> any:  # PatternGeometry
    """
    Apply grading to a pattern geometry.
    
    Grading must not alter the base pattern logic, only scale measurements.
    """
    # This would apply grading transformations to the geometry
    # For now, this is a placeholder that would need geometry operations
    # to scale pattern pieces based on graded measurements
    return pattern_geometry


def batch_generate_sizes(
    base_measurements: Dict[str, float],
    grading_table: GradingTable,
    target_sizes: List[str],
) -> Dict[str, Dict[str, float]]:
    """
    Generate measurements for multiple sizes in a batch.
    
    Args:
        base_measurements: Base size measurements
        grading_table: Grading table to apply
        target_sizes: List of size names to generate
    
    Returns:
        Dict mapping size names to their graded measurements
    """
    results = {}
    base_size_index = grading_table.size_range.sizes.index(
        grading_table.size_range.base_size
    )
    
    for target_size in target_sizes:
        if target_size not in grading_table.size_range.sizes:
            continue
        target_index = grading_table.size_range.sizes.index(target_size)
        size_offset = target_index - base_size_index
        
        graded = calculate_graded_measurements(
            base_measurements, grading_table, size_offset
        )
        results[target_size] = graded
    
    return results

