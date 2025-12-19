from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List

from ..formulas.evaluator import evaluate_formula
from ..formulas.models import FormulaContext
from ..geometry.patterns import PatternGeometry, PatternPiece
from ..geometry.primitives import LineSegment, Point2D, Arc, Spline
from .models import RuleGraphConfig, RuleNode, RuleType


class RuleGraphError(RuntimeError):
    pass


def _topological_sort(nodes: List[RuleNode]) -> List[RuleNode]:
    indegree: Dict[str, int] = defaultdict(int)
    adjacency: Dict[str, List[str]] = defaultdict(list)
    node_by_id: Dict[str, RuleNode] = {n.id: n for n in nodes}

    for node in nodes:
        for dep in node.inputs:
            adjacency[dep].append(node.id)
            indegree[node.id] += 1

    queue: deque[str] = deque([nid for nid in node_by_id if indegree[nid] == 0])
    ordered: List[RuleNode] = []

    while queue:
        nid = queue.popleft()
        ordered.append(node_by_id[nid])
        for succ in adjacency[nid]:
            indegree[succ] -= 1
            if indegree[succ] == 0:
                queue.append(succ)

    if len(ordered) != len(nodes):
        raise RuleGraphError("Rule graph contains cycles or unreachable nodes")
    return ordered


def execute_rule_graph(
    graph: RuleGraphConfig,
    context_variables: Dict[str, float],
    geometry: PatternGeometry | None = None,
) -> PatternGeometry:
    """
    Execute the rule graph against the given context, producing geometry.

    This is a minimal MVP implementation. It supports:
    - COMPUTE_VALUE nodes
    - CONSTRUCT_POINT nodes
    - CONSTRUCT_LINE nodes
    """
    if geometry is None:
        geometry = PatternGeometry()

    variables = dict(context_variables)
    pieces: Dict[str, PatternPiece] = {}

    ordered_nodes = _topological_sort(graph.nodes)

    for node in ordered_nodes:
        if node.type == RuleType.COMPUTE_VALUE:
            if not node.formula:
                raise RuleGraphError(f"Node {node.id} missing formula")
            value = evaluate_formula(node.formula, FormulaContext(variables=variables))
            if len(node.outputs) != 1:
                raise RuleGraphError(
                    f"COMPUTE_VALUE node {node.id} must have exactly one output"
                )
            variables[node.outputs[0]] = value

        elif node.type == RuleType.CONSTRUCT_POINT:
            x_name = node.params.get("x_var")
            y_name = node.params.get("y_var")
            label = node.params.get("label")
            if not isinstance(x_name, str) or not isinstance(y_name, str):
                raise RuleGraphError(f"CONSTRUCT_POINT {node.id} missing x_var/y_var")
            point = Point2D(x=variables[x_name], y=variables[y_name], label=label)
            if len(node.outputs) != 1:
                raise RuleGraphError(
                    f"CONSTRUCT_POINT node {node.id} must have exactly one output"
                )
            variables[node.outputs[0]] = point  # type: ignore[assignment]

        elif node.type == RuleType.CONSTRUCT_LINE:
            start_key = node.params.get("start_point")
            end_key = node.params.get("end_point")
            piece_id = node.params.get("piece_id", "piece-0")
            if not isinstance(start_key, str) or not isinstance(end_key, str):
                raise RuleGraphError(f"CONSTRUCT_LINE {node.id} missing point keys")
            start = variables[start_key]
            end = variables[end_key]
            if not isinstance(start, Point2D) or not isinstance(end, Point2D):
                raise RuleGraphError(
                    f"CONSTRUCT_LINE {node.id} requires Point2D variables"
                )
            line = LineSegment(start=start, end=end, is_guide=False)
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            piece.lines.append(line)

        elif node.type == RuleType.CONSTRUCT_ARC:
            center_key = node.params.get("center")
            radius_key = node.params.get("radius")
            start_angle_key = node.params.get("start_angle")
            end_angle_key = node.params.get("end_angle")
            piece_id = node.params.get("piece_id", "piece-0")
            
            # Center can be a point variable or direct x/y values
            if isinstance(center_key, str):
                center = variables[center_key]
                if not isinstance(center, Point2D):
                    raise RuleGraphError(f"CONSTRUCT_ARC {node.id} center must be Point2D")
            else:
                # Direct x/y values
                center_x = node.params.get("center_x", 0.0)
                center_y = node.params.get("center_y", 0.0)
                center = Point2D(x=float(center_x), y=float(center_y))
            
            # Radius can be a variable or direct value
            if isinstance(radius_key, str):
                radius = variables[radius_key]
            else:
                radius = float(node.params.get("radius", 0.0))
            
            # Angles can be variables or direct values
            if isinstance(start_angle_key, str):
                start_angle = variables[start_angle_key]
            else:
                start_angle = float(node.params.get("start_angle", 0.0))
            
            if isinstance(end_angle_key, str):
                end_angle = variables[end_angle_key]
            else:
                end_angle = float(node.params.get("end_angle", 0.0))
            
            arc = Arc(center=center, radius=float(radius), start_angle=float(start_angle), end_angle=float(end_angle))
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            piece.arcs.append(arc)
            
            if len(node.outputs) == 1:
                variables[node.outputs[0]] = arc  # type: ignore[assignment]

        elif node.type == RuleType.CONSTRUCT_SPLINE:
            control_points_keys = node.params.get("control_points", [])
            piece_id = node.params.get("piece_id", "piece-0")
            
            if not isinstance(control_points_keys, list):
                raise RuleGraphError(f"CONSTRUCT_SPLINE {node.id} control_points must be a list")
            
            control_points = []
            for cp_key in control_points_keys:
                if isinstance(cp_key, str):
                    point = variables[cp_key]
                    if not isinstance(point, Point2D):
                        raise RuleGraphError(f"CONSTRUCT_SPLINE {node.id} control point must be Point2D")
                    control_points.append(point)
                else:
                    raise RuleGraphError(f"CONSTRUCT_SPLINE {node.id} control_points must be variable names")
            
            if len(control_points) < 2:
                raise RuleGraphError(f"CONSTRUCT_SPLINE {node.id} needs at least 2 control points")
            
            spline = Spline(control_points=control_points)
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            piece.splines.append(spline)
            
            if len(node.outputs) == 1:
                variables[node.outputs[0]] = spline  # type: ignore[assignment]

        elif node.type == RuleType.CONSTRUCT_GRAIN_LINE:
            start_key = node.params.get("start_point")
            end_key = node.params.get("end_point")
            piece_id = node.params.get("piece_id", "piece-0")
            
            if not isinstance(start_key, str) or not isinstance(end_key, str):
                raise RuleGraphError(f"CONSTRUCT_GRAIN_LINE {node.id} missing start_point/end_point")
            
            start = variables[start_key]
            end = variables[end_key]
            if not isinstance(start, Point2D) or not isinstance(end, Point2D):
                raise RuleGraphError(f"CONSTRUCT_GRAIN_LINE {node.id} requires Point2D variables")
            
            grain_line = LineSegment(start=start, end=end, is_guide=False)
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            piece.grain_line = grain_line

        elif node.type == RuleType.CONSTRUCT_DART:
            apex_key = node.params.get("apex_point")
            left_key = node.params.get("left_point")
            right_key = node.params.get("right_point")
            piece_id = node.params.get("piece_id", "piece-0")
            
            if not all(isinstance(k, str) for k in [apex_key, left_key, right_key]):
                raise RuleGraphError(f"CONSTRUCT_DART {node.id} missing apex_point/left_point/right_point")
            
            apex = variables[apex_key]
            left = variables[left_key]
            right = variables[right_key]
            
            if not all(isinstance(p, Point2D) for p in [apex, left, right]):
                raise RuleGraphError(f"CONSTRUCT_DART {node.id} requires Point2D variables")
            
            # Create dart as two lines from apex to left and right points
            dart_left = LineSegment(start=apex, end=left, is_guide=False)
            dart_right = LineSegment(start=apex, end=right, is_guide=False)
            
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            piece.lines.append(dart_left)
            piece.lines.append(dart_right)

        elif node.type == RuleType.CONSTRUCT_NOTCH:
            location_key = node.params.get("location_point")
            piece_id = node.params.get("piece_id", "piece-0")
            notch_type = node.params.get("notch_type", "standard")
            
            if not isinstance(location_key, str):
                raise RuleGraphError(f"CONSTRUCT_NOTCH {node.id} missing location_point")
            
            location = variables[location_key]
            if not isinstance(location, Point2D):
                raise RuleGraphError(f"CONSTRUCT_NOTCH {node.id} location_point must be Point2D")
            
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            # Store notches in piece metadata
            if 'notches' not in piece.metadata:
                piece.metadata['notches'] = []
            piece.metadata['notches'].append({
                'location': location,
                'type': notch_type
            })

        elif node.type == RuleType.CONSTRUCT_PIECE_BOUNDARY:
            boundary_points_keys = node.params.get("boundary_points", [])
            piece_id = node.params.get("piece_id", "piece-0")
            
            if not isinstance(boundary_points_keys, list):
                raise RuleGraphError(f"CONSTRUCT_PIECE_BOUNDARY {node.id} boundary_points must be a list")
            
            boundary_points = []
            for bp_key in boundary_points_keys:
                if isinstance(bp_key, str):
                    point = variables[bp_key]
                    if not isinstance(point, Point2D):
                        raise RuleGraphError(f"CONSTRUCT_PIECE_BOUNDARY {node.id} boundary point must be Point2D")
                    boundary_points.append(point)
            
            if len(boundary_points) < 3:
                raise RuleGraphError(f"CONSTRUCT_PIECE_BOUNDARY {node.id} needs at least 3 points")
            
            # Create closed boundary by connecting points
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            for i in range(len(boundary_points)):
                start = boundary_points[i]
                end = boundary_points[(i + 1) % len(boundary_points)]  # Close the loop
                boundary_line = LineSegment(start=start, end=end, is_guide=False)
                piece.lines.append(boundary_line)
            
            # Store boundary points in piece
            piece.points = boundary_points

        elif node.type == RuleType.SET_PIECE_METADATA:
            piece_id = node.params.get("piece_id", "piece-0")
            name = node.params.get("name")
            orientation = node.params.get("orientation")
            cut_count = node.params.get("cut_count")
            
            piece = pieces.setdefault(piece_id, PatternPiece(id=piece_id, name=piece_id))
            
            if name:
                piece.name = str(name)
            
            # Store metadata in piece metadata dict
            if orientation:
                piece.metadata['orientation'] = str(orientation)
            if cut_count is not None:
                piece.metadata['cut_count'] = int(cut_count)

        elif node.type == RuleType.APPLY_TRANSFORM:
            # High-level transform application is handled at a different level;
            # for MVP we treat this as a no-op.
            continue

        else:
            # Other node types can be added incrementally.
            continue

    # Collect pieces in deterministic order
    geometry.pieces = [pieces[k] for k in sorted(pieces.keys())]
    return geometry







