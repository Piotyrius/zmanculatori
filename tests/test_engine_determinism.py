from __future__ import annotations

from engine import PatternRequest, generate_pattern
from engine.measurements.models import MeasurementProfile


def test_generate_pattern_does_not_crash_for_empty_graph() -> None:
    profile = MeasurementProfile(values={"chest": 900.0}, unit="mm")
    req = PatternRequest(
        measurement_profile=profile,
        garment_type="bodice",
        fit="regular",
        category="adult",
        drafting_school_id="school-1",
        drafting_school_version="1.0",
        block_id="block-1",
        block_version="1.0",
        rule_graph_id="graph-1",
        rule_graph_version="1.0",
    )

    geometry = generate_pattern(req)
    assert geometry.units == "mm"




