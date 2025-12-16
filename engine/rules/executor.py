from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List

from ..formulas.evaluator import evaluate_formula
from ..formulas.models import FormulaContext
from ..geometry.patterns import PatternGeometry, PatternPiece
from ..geometry.primitives import LineSegment, Point2D
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



