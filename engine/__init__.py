"""
Core drafting engine package.

This package is intentionally framework-agnostic and contains no references
to FastAPI, Celery, databases, or subscription logic.
"""

from .interface import PatternRequest, PatternGeometry, ExportOptions, ExportBundle, generate_pattern, export_pattern

__all__ = [
    "PatternRequest",
    "PatternGeometry",
    "ExportOptions",
    "ExportBundle",
    "generate_pattern",
    "export_pattern",
]












