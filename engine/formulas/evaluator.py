from __future__ import annotations

import ast
import math
from typing import Any, Dict, Optional

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
    ast.Constant,  # Python 3.8+ uses Constant instead of Num
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
    
    Supports all formula types including conditional formulas.
    """
    def _eval(node: ast.AST, ctx: FormulaContext) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body, ctx)
        if isinstance(node, ast.Num):
            return float(node.n)
        if isinstance(node, ast.Constant):  # Python 3.8+ uses Constant instead of Num
            return float(node.value)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left, ctx)
            right = _eval(node.right, ctx)
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
            operand = _eval(node.operand, ctx)
            if isinstance(node.op, ast.USub):
                return -operand
        if isinstance(node, ast.Name):
            try:
                return float(ctx.variables[node.id])
            except KeyError as exc:
                raise FormulaError(f"Unknown variable in formula: {node.id}") from exc
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise FormulaError("Only simple function calls are allowed")
            func_name = node.func.id
            if func_name not in _ALLOWED_FUNCS:
                raise FormulaError(f"Disallowed function: {func_name}")
            func = _ALLOWED_FUNCS[func_name]
            args = [_eval(arg, ctx) for arg in node.args]
            return float(func(*args))
        raise FormulaError(f"Unsupported expression element: {type(node).__name__}")
    
    # Check if this is a conditional formula
    from .models import FormulaType
    if formula.formula_type == FormulaType.CONDITIONAL and formula.condition:
        # Evaluate condition first
        try:
            condition_parsed = ast.parse(formula.condition, mode="eval")
            _validate_ast(condition_parsed)
            condition_result = _eval(condition_parsed.body, context)
            
            # Check threshold if provided
            if formula.threshold is not None:
                if not (condition_result >= formula.threshold):
                    # Condition not met, return default or raise
                    raise FormulaError(
                        f"Condition not met: {formula.condition} >= {formula.threshold}"
                    )
            elif not condition_result:
                # Boolean condition false
                raise FormulaError(f"Condition not met: {formula.condition}")
        except Exception as exc:
            if isinstance(exc, FormulaError):
                raise
            raise FormulaError(f"Invalid condition: {formula.condition}") from exc
    
    try:
        parsed = ast.parse(formula.expression, mode="eval")
    except SyntaxError as exc:
        raise FormulaError(f"Invalid formula syntax: {formula.expression}") from exc

    _validate_ast(parsed)

    value = _eval(parsed.body, context)
    if math.isnan(value) or math.isinf(value):
        raise FormulaError("Formula evaluation produced invalid numeric result")
    return value


def evaluate_conditional_formula(
    formula: Formula,
    context: FormulaContext,
    default: Optional[float] = None
) -> Optional[float]:
    """
    Evaluate a conditional formula, returning default if condition not met.
    """
    try:
        return evaluate_formula(formula, context)
    except FormulaError:
        if default is not None:
            return default
        raise


def calculate_derived_measurement(
    formula: Formula,
    context: FormulaContext
) -> Dict[str, float]:
    """
    Calculate a derived measurement using a formula.
    Returns a dict with the output_name and calculated value.
    """
    value = evaluate_formula(formula, context)
    output_name = formula.output_name or "derived_value"
    return {output_name: value}






