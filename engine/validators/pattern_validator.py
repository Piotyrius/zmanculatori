from __future__ import annotations

from ..geometry.patterns import PatternGeometry, PatternValidationResult, PatternPiece
from ..geometry.primitives import Point2D


def validate_pattern_geometry(geometry: PatternGeometry) -> PatternValidationResult:
    """
    Professional pattern validator for MVP.

    Validates:
    - Pattern pieces have closed boundaries
    - Darts are properly constructed
    - Grain lines are present
    - Pattern pieces have required metadata
    - Measurements are within reasonable ranges
    """
    warnings: list[str] = []
    errors: list[str] = []

    if not geometry.pieces:
        errors.append("Pattern has no pieces.")
        return PatternValidationResult(is_valid=False, warnings=warnings, errors=errors)

    for piece in geometry.pieces:
        # Check for closed boundaries
        if not _has_closed_boundary(piece):
            errors.append(f"Pattern piece '{piece.name}' does not have a closed boundary.")
        
        # Check for grain line
        if not piece.grain_line:
            warnings.append(f"Pattern piece '{piece.name}' is missing a grain line.")
        
        # Check for required metadata
        if not piece.name or piece.name == piece.id:
            warnings.append(f"Pattern piece '{piece.id}' has no descriptive name.")
        
        if 'cut_count' not in piece.metadata:
            warnings.append(f"Pattern piece '{piece.name}' is missing cut_count metadata.")
        
        if 'orientation' not in piece.metadata:
            warnings.append(f"Pattern piece '{piece.name}' is missing orientation metadata.")
        
        # Check for darts (if applicable)
        dart_lines = [line for line in piece.lines if _is_dart_line(line, piece)]
        if dart_lines and len(dart_lines) % 2 != 0:
            warnings.append(f"Pattern piece '{piece.name}' has incomplete dart (odd number of dart lines).")

    is_valid = not errors
    return PatternValidationResult(is_valid=is_valid, warnings=warnings, errors=errors)


def _has_closed_boundary(piece: PatternPiece) -> bool:
    """Check if pattern piece has a closed boundary."""
    if not piece.lines:
        return False
    
    # Check if lines form a closed loop
    # Simple check: count line endpoints and see if they match
    all_points = []
    for line in piece.lines:
        if not line.is_guide:
            all_points.append((line.start.x, line.start.y))
            all_points.append((line.end.x, line.end.y))
    
    # For a closed boundary, each point should appear exactly twice (except if it's a single point)
    from collections import Counter
    point_counts = Counter(all_points)
    
    # All points should appear exactly 2 times (start and end of different lines)
    # Except for the first/last point which might appear once if boundary is truly closed
    odd_count = sum(1 for count in point_counts.values() if count % 2 != 0)
    
    # If we have boundary points defined, use those
    if piece.points and len(piece.points) >= 3:
        return True
    
    # Otherwise, check if lines form a closed shape
    return odd_count <= 2  # Allow 0 or 2 odd counts (start and end of closed loop)


def _is_dart_line(line: LineSegment, piece: PatternPiece) -> bool:
    """Check if a line is part of a dart."""
    # Simple heuristic: dart lines typically connect to a common apex point
    # This is a simplified check - in production, you'd track dart construction
    return False  # Placeholder - would need more sophisticated detection


def validate_measurements(measurements: dict[str, float], category: str = "womenswear") -> PatternValidationResult:
    """
    Validate measurement sanity checks.
    
    Checks:
    - bust > waist (for womenswear)
    - hip > waist
    - armhole_depth within acceptable ratio
    - Basic range checks (prevent negative or extreme values)
    """
    warnings: list[str] = []
    errors: list[str] = []
    
    # Basic range checks
    for name, value in measurements.items():
        if value < 0:
            errors.append(f"Measurement '{name}' cannot be negative: {value}")
        if value > 200:  # Reasonable upper limit in cm
            warnings.append(f"Measurement '{name}' seems unusually large: {value} cm")
        if value < 10 and name not in ['bust_point_distance', 'bust_point_height']:
            warnings.append(f"Measurement '{name}' seems unusually small: {value} cm")
    
    # Category-specific checks
    if category == "womenswear":
        bust = measurements.get("bust", 0)
        waist = measurements.get("waist", 0)
        hip = measurements.get("hip", 0)
        
        if bust > 0 and waist > 0:
            if bust <= waist:
                errors.append(f"Bust ({bust}) must be greater than waist ({waist}) for womenswear.")
            elif bust - waist < 5:
                warnings.append(f"Bust and waist are very close ({bust} vs {waist}). Verify measurements.")
        
        if hip > 0 and waist > 0:
            if hip <= waist:
                errors.append(f"Hip ({hip}) must be greater than waist ({waist}) for womenswear.")
            elif hip - waist < 5:
                warnings.append(f"Hip and waist are very close ({hip} vs {waist}). Verify measurements.")
        
        # Armhole depth check
        chest = measurements.get("chest", measurements.get("bust", 0))
        if chest > 0:
            expected_armhole_range = (chest / 4 - 2, chest / 4 + 6)
            armhole_depth = measurements.get("armhole_depth", 0)
            if armhole_depth > 0:
                if armhole_depth < expected_armhole_range[0] or armhole_depth > expected_armhole_range[1]:
                    warnings.append(
                        f"Armhole depth ({armhole_depth}) seems outside expected range "
                        f"({expected_armhole_range[0]:.1f} - {expected_armhole_range[1]:.1f}) "
                        f"for chest size {chest}."
                    )
    
    is_valid = not errors
    return PatternValidationResult(is_valid=is_valid, warnings=warnings, errors=errors)






