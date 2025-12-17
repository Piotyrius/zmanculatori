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
                    # === COMPUTE MEASUREMENTS ===
                    {
                        "id": "compute_armhole_depth",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "bust / 4 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["armhole_depth"],
                    },
                    {
                        "id": "compute_neck_width",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "bust / 20 + 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["neck_width"],
                    },
                    {
                        "id": "compute_shoulder_slope",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "back_length / 10",
                            "formula_type": "proportional",
                        },
                        "outputs": ["shoulder_slope"],
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
                    {
                        "id": "compute_front_width",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "bust / 2 + 1",
                            "formula_type": "proportional",
                        },
                        "outputs": ["front_width"],
                    },
                    {
                        "id": "compute_back_width",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "bust / 2 - 1",
                            "formula_type": "proportional",
                        },
                        "outputs": ["back_width"],
                    },
                    {
                        "id": "compute_dart_width",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "dart_intake / 2",
                            "formula_type": "derived",
                        },
                        "outputs": ["dart_width"],
                    },
                    {
                        "id": "compute_zero",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "0",
                            "formula_type": "proportional",
                        },
                        "outputs": ["zero"],
                    },
                    # === FRONT BODICE POINTS ===
                    {
                        "id": "front_origin",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "back_length",
                            "label": "Front Origin"
                        },
                        "outputs": ["front_origin"],
                    },
                    {
                        "id": "front_shoulder_point",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "back_length",
                            "label": "Front Shoulder"
                        },
                        "outputs": ["front_shoulder_point"],
                    },
                    {
                        "id": "front_neck_point",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "neck_width",
                            "y_var": "back_length",
                            "label": "Front Neck"
                        },
                        "outputs": ["front_neck_point"],
                    },
                    {
                        "id": "front_armhole_top",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "armhole_depth",
                            "label": "Front Armhole Top"
                        },
                        "outputs": ["front_armhole_top"],
                    },
                    {
                        "id": "compute_front_armhole_bottom_y",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "armhole_depth / 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["front_armhole_bottom_y"],
                    },
                    {
                        "id": "front_armhole_bottom",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "front_armhole_bottom_y",
                            "label": "Front Armhole Bottom"
                        },
                        "outputs": ["front_armhole_bottom"],
                    },
                    {
                        "id": "front_waist_center",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "zero",
                            "label": "Front Waist Center"
                        },
                        "outputs": ["front_waist_center"],
                    },
                    {
                        "id": "front_waist_side",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "zero",
                            "y_var": "zero",
                            "label": "Front Waist Side"
                        },
                        "outputs": ["front_waist_side"],
                    },
                    {
                        "id": "compute_front_dart_apex_y",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "armhole_depth / 2 + dart_intake",
                            "formula_type": "derived",
                        },
                        "outputs": ["front_dart_apex_y"],
                    },
                    {
                        "id": "front_dart_apex",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_width",
                            "y_var": "front_dart_apex_y",
                            "label": "Front Dart Apex"
                        },
                        "outputs": ["front_dart_apex"],
                    },
                    {
                        "id": "compute_front_dart_left_x",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "front_width - dart_width",
                            "formula_type": "derived",
                        },
                        "outputs": ["front_dart_left_x"],
                    },
                    {
                        "id": "front_dart_left",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_dart_left_x",
                            "y_var": "zero",
                            "label": "Front Dart Left"
                        },
                        "outputs": ["front_dart_left"],
                    },
                    {
                        "id": "compute_front_dart_right_x",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "front_width + dart_width",
                            "formula_type": "derived",
                        },
                        "outputs": ["front_dart_right_x"],
                    },
                    {
                        "id": "front_dart_right",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "front_dart_right_x",
                            "y_var": "zero",
                            "label": "Front Dart Right"
                        },
                        "outputs": ["front_dart_right"],
                    },
                    # === BACK BODICE POINTS ===
                    {
                        "id": "back_origin",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "zero",
                            "y_var": "back_length",
                            "label": "Back Origin"
                        },
                        "outputs": ["back_origin"],
                    },
                    {
                        "id": "back_shoulder_point",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_width",
                            "y_var": "back_length",
                            "label": "Back Shoulder"
                        },
                        "outputs": ["back_shoulder_point"],
                    },
                    {
                        "id": "back_neck_point",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "neck_width",
                            "y_var": "back_length",
                            "label": "Back Neck"
                        },
                        "outputs": ["back_neck_point"],
                    },
                    {
                        "id": "back_armhole_top",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_width",
                            "y_var": "armhole_depth",
                            "label": "Back Armhole Top"
                        },
                        "outputs": ["back_armhole_top"],
                    },
                    {
                        "id": "compute_back_armhole_bottom_y",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "armhole_depth / 2",
                            "formula_type": "proportional",
                        },
                        "outputs": ["back_armhole_bottom_y"],
                    },
                    {
                        "id": "back_armhole_bottom",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "0",
                            "y_var": "back_armhole_bottom_y",
                            "label": "Back Armhole Bottom"
                        },
                        "outputs": ["back_armhole_bottom"],
                    },
                    {
                        "id": "back_waist_center",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_width",
                            "y_var": "zero",
                            "label": "Back Waist Center"
                        },
                        "outputs": ["back_waist_center"],
                    },
                    {
                        "id": "back_waist_side",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "zero",
                            "y_var": "zero",
                            "label": "Back Waist Side"
                        },
                        "outputs": ["back_waist_side"],
                    },
                    {
                        "id": "compute_back_dart_apex_y",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "armhole_depth / 2 + dart_intake",
                            "formula_type": "derived",
                        },
                        "outputs": ["back_dart_apex_y"],
                    },
                    {
                        "id": "back_dart_apex",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_width",
                            "y_var": "back_dart_apex_y",
                            "label": "Back Dart Apex"
                        },
                        "outputs": ["back_dart_apex"],
                    },
                    {
                        "id": "compute_back_dart_left_x",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "back_width - dart_width",
                            "formula_type": "derived",
                        },
                        "outputs": ["back_dart_left_x"],
                    },
                    {
                        "id": "back_dart_left",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_dart_left_x",
                            "y_var": "zero",
                            "label": "Back Dart Left"
                        },
                        "outputs": ["back_dart_left"],
                    },
                    {
                        "id": "compute_back_dart_right_x",
                        "type": "COMPUTE_VALUE",
                        "formula": {
                            "expression": "back_width + dart_width",
                            "formula_type": "derived",
                        },
                        "outputs": ["back_dart_right_x"],
                    },
                    {
                        "id": "back_dart_right",
                        "type": "CONSTRUCT_POINT",
                        "params": {
                            "x_var": "back_dart_right_x",
                            "y_var": "zero",
                            "label": "Back Dart Right"
                        },
                        "outputs": ["back_dart_right"],
                    },
                    # === FRONT BODICE CONSTRUCTION ===
                    {
                        "id": "front_shoulder_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["front_neck_point", "front_shoulder_point"],
                        "params": {
                            "start_point": "front_neck_point",
                            "end_point": "front_shoulder_point",
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_armhole_curve",
                        "type": "CONSTRUCT_SPLINE",
                        "inputs": ["front_shoulder_point", "front_armhole_top", "front_armhole_bottom"],
                        "params": {
                            "control_points": ["front_shoulder_point", "front_armhole_top", "front_armhole_bottom"],
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_side_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["front_armhole_bottom", "front_waist_side"],
                        "params": {
                            "start_point": "front_armhole_bottom",
                            "end_point": "front_waist_side",
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_waist_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["front_waist_side", "front_waist_center"],
                        "params": {
                            "start_point": "front_waist_side",
                            "end_point": "front_waist_center",
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_neckline_curve",
                        "type": "CONSTRUCT_SPLINE",
                        "inputs": ["front_neck_point", "front_origin"],
                        "params": {
                            "control_points": ["front_neck_point", "front_origin"],
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_waist_dart",
                        "type": "CONSTRUCT_DART",
                        "inputs": ["front_dart_apex", "front_dart_left", "front_dart_right"],
                        "params": {
                            "dart_type": "waist",
                            "apex_point": "front_dart_apex",
                            "left_point": "front_dart_left",
                            "right_point": "front_dart_right",
                            "intake_value": "dart_intake",
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_grain_line",
                        "type": "CONSTRUCT_GRAIN_LINE",
                        "inputs": ["front_origin", "front_waist_center"],
                        "params": {
                            "start_point": "front_origin",
                            "end_point": "front_waist_center",
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_boundary",
                        "type": "CONSTRUCT_PIECE_BOUNDARY",
                        "inputs": ["front_neck_point", "front_shoulder_point", "front_armhole_bottom", "front_waist_side", "front_waist_center"],
                        "params": {
                            "boundary_points": ["front_neck_point", "front_shoulder_point", "front_armhole_bottom", "front_waist_side", "front_waist_center"],
                            "piece_id": "bodice-front"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_notch_shoulder",
                        "type": "CONSTRUCT_NOTCH",
                        "inputs": ["front_shoulder_point"],
                        "params": {
                            "location_point": "front_shoulder_point",
                            "piece_id": "bodice-front",
                            "notch_type": "standard"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_notch_armhole",
                        "type": "CONSTRUCT_NOTCH",
                        "inputs": ["front_armhole_bottom"],
                        "params": {
                            "location_point": "front_armhole_bottom",
                            "piece_id": "bodice-front",
                            "notch_type": "standard"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "front_metadata",
                        "type": "SET_PIECE_METADATA",
                        "params": {
                            "piece_id": "bodice-front",
                            "name": "Bodice Front",
                            "orientation": "vertical",
                            "cut_count": 1
                        },
                        "outputs": [],
                    },
                    # === BACK BODICE CONSTRUCTION ===
                    {
                        "id": "back_shoulder_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["back_neck_point", "back_shoulder_point"],
                        "params": {
                            "start_point": "back_neck_point",
                            "end_point": "back_shoulder_point",
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_armhole_curve",
                        "type": "CONSTRUCT_SPLINE",
                        "inputs": ["back_shoulder_point", "back_armhole_top", "back_armhole_bottom"],
                        "params": {
                            "control_points": ["back_shoulder_point", "back_armhole_top", "back_armhole_bottom"],
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_side_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["back_armhole_bottom", "back_waist_side"],
                        "params": {
                            "start_point": "back_armhole_bottom",
                            "end_point": "back_waist_side",
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_waist_seam",
                        "type": "CONSTRUCT_LINE",
                        "inputs": ["back_waist_side", "back_waist_center"],
                        "params": {
                            "start_point": "back_waist_side",
                            "end_point": "back_waist_center",
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_neckline_curve",
                        "type": "CONSTRUCT_SPLINE",
                        "inputs": ["back_neck_point", "back_origin"],
                        "params": {
                            "control_points": ["back_neck_point", "back_origin"],
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_waist_dart",
                        "type": "CONSTRUCT_DART",
                        "inputs": ["back_dart_apex", "back_dart_left", "back_dart_right"],
                        "params": {
                            "dart_type": "waist",
                            "apex_point": "back_dart_apex",
                            "left_point": "back_dart_left",
                            "right_point": "back_dart_right",
                            "intake_value": "dart_intake",
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_grain_line",
                        "type": "CONSTRUCT_GRAIN_LINE",
                        "inputs": ["back_origin", "back_waist_center"],
                        "params": {
                            "start_point": "back_origin",
                            "end_point": "back_waist_center",
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_boundary",
                        "type": "CONSTRUCT_PIECE_BOUNDARY",
                        "inputs": ["back_neck_point", "back_shoulder_point", "back_armhole_bottom", "back_waist_side", "back_waist_center"],
                        "params": {
                            "boundary_points": ["back_neck_point", "back_shoulder_point", "back_armhole_bottom", "back_waist_side", "back_waist_center"],
                            "piece_id": "bodice-back"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_notch_shoulder",
                        "type": "CONSTRUCT_NOTCH",
                        "inputs": ["back_shoulder_point"],
                        "params": {
                            "location_point": "back_shoulder_point",
                            "piece_id": "bodice-back",
                            "notch_type": "standard"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_notch_armhole",
                        "type": "CONSTRUCT_NOTCH",
                        "inputs": ["back_armhole_bottom"],
                        "params": {
                            "location_point": "back_armhole_bottom",
                            "piece_id": "bodice-back",
                            "notch_type": "standard"
                        },
                        "outputs": [],
                    },
                    {
                        "id": "back_metadata",
                        "type": "SET_PIECE_METADATA",
                        "params": {
                            "piece_id": "bodice-back",
                            "name": "Bodice Back",
                            "orientation": "vertical",
                            "cut_count": 1
                        },
                        "outputs": [],
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

