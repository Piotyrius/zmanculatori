from __future__ import annotations

import ast
import math
from typing import Any, Dict

from .models import Formula, FormulaContext, FormulaError


_ALLOWED_FUNCS: Dict[str, Any] = {
    "min": min,
    "max": max,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
}

_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.Num,
    ast.Name,
    ast.Call,
    ast.Load,
)


def _validate_ast(node: ast.AST, depth: int = 0, max_depth: int = 16) -> None:
    if depth > max_depth:
        raise FormulaError("Formula too deeply nested")

    if not isinstance(node, _ALLOWED_NODES):
        raise FormulaError(f"Disallowed expression element: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _validate_ast(child, depth + 1, max_depth=max_depth)


def evaluate_formula(formula: Formula, context: FormulaContext) -> float:
    """
    Safely evaluate a formula expression against the provided context.
    """
    try:
        parsed = ast.parse(formula.expression, mode="eval")
    except SyntaxError as exc:
        raise FormulaError(f"Invalid formula syntax: {formula.expression}") from exc

    _validate_ast(parsed)

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):
            return float(node.n)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left**right
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
        if isinstance(node, ast.Name):
            try:
                return float(context.variables[node.id])
            except KeyError as exc:
                raise FormulaError(f"Unknown variable in formula: {node.id}") from exc
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise FormulaError("Only simple function calls are allowed")
            func_name = node.func.id
            if func_name not in _ALLOWED_FUNCS:
                raise FormulaError(f"Disallowed function: {func_name}")
            func = _ALLOWED_FUNCS[func_name]
            args = [_eval(arg) for arg in node.args]
            return float(func(*args))
        raise FormulaError(f"Unsupported expression element: {type(node).__name__}")

    value = _eval(parsed)
    if math.isnan(value) or math.isinf(value):
        raise FormulaError("Formula evaluation produced invalid numeric result")
    return value





