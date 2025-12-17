from __future__ import annotations

from ..geometry.patterns import PatternGeometry, PatternValidationResult


def validate_pattern_geometry(geometry: PatternGeometry) -> PatternValidationResult:
    """
    Minimal pattern validator for MVP.

    For now, it only checks that at least one piece exists and that each piece
    has at least one line; more sophisticated checks can be added incrementally.
    """
    warnings: list[str] = []
    errors: list[str] = []

    if not geometry.pieces:
        warnings.append("Pattern has no pieces.")

    for piece in geometry.pieces:
        if not piece.lines:
            warnings.append(f"Pattern piece '{piece.name}' has no line segments.")

    is_valid = not errors
    return PatternValidationResult(is_valid=is_valid, warnings=warnings, errors=errors)






