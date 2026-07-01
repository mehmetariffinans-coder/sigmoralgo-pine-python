"""AST Node definitions for Pine Script with TradingView Support"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int = 0

# ============ LITERALS ============

@dataclass
class Number(ASTNode):
    """Number literal"""
    value: float = 0.0

@dataclass
class String(ASTNode):
    """String literal"""
    value: str = ""

@dataclass
class Boolean(ASTNode):
    """Boolean literal"""
    value: bool = False

@dataclass
class Identifier(ASTNode):
    """Variable/function identifier"""
    name: str = ""

@dataclass
class NA(ASTNode):
    """NA (Not Available) literal"""
    pass

# ============ PINE SERIES ============

@dataclass
class SeriesBuiltin(ASTNode):
    """Pine Script built-in series (close, open, high, low, volume, etc.)"""
    name: str = ""  # close, open, high, low, volume, hl2, hlc3, ohlc4, time, bar_index
    offset: Optional[ASTNode] = None  # close[1] için offset

# ============ EXPRESSIONS ============

@dataclass
class BinaryOp(ASTNode):
    """Binary operation (e.g., a + b)"""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None

@dataclass
class UnaryOp(ASTNode):
    """Unary operation (e.g., -a, not a)"""
    operator: str = ""
    operand: ASTNode = None

@dataclass
class TernaryOp(ASTNode):
    """Ternary operation (e.g., a ? b : c)"""
    condition: ASTNode = None
    true_expr: ASTNode = None
    false_expr: ASTNode = None

@dataclass
class Assignment(ASTNode):
    """Variable assignment (e.g., x = 5)"""
    target: str = ""
    value: ASTNode = None
    operator: str = "="  # =, +=, -=, etc.

@dataclass
class MemberAccess(ASTNode):
    """Member access (e.g., ta.sma, obj.method)"""
    object: ASTNode = None
    member: str = ""

@dataclass
class FunctionCall(ASTNode):
    """Function call (e.g., func(a, b))"""
    name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)

@dataclass
class MethodCall(ASTNode):
    """Method call (e.g., obj.method(args))"""
    object: ASTNode = None
    method: str = ""
    arguments: List[ASTNode] = field(default_factory=list)

@dataclass
class ArrayAccess(ASTNode):
    """Array access (e.g., arr[i])"""
    array: ASTNode = None
    index: ASTNode = None

# ============ STATEMENTS ============

@dataclass
class Block(ASTNode):
    """Code block"""
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class IfStatement(ASTNode):
    """If statement"""
    condition: ASTNode = None
    then_body: ASTNode = None
    else_body: Optional[ASTNode] = None

@dataclass
class ForStatement(ASTNode):
    """For loop"""
    init: Optional[ASTNode] = None
    condition: Optional[ASTNode] = None
    update: Optional[ASTNode] = None
    body: ASTNode = None

@dataclass
class WhileStatement(ASTNode):
    """While loop"""
    condition: ASTNode = None
    body: ASTNode = None

@dataclass
class ReturnStatement(ASTNode):
    """Return statement"""
    value: Optional[ASTNode] = None

@dataclass
class BreakStatement(ASTNode):
    """Break statement"""
    pass

@dataclass
class ContinueStatement(ASTNode):
    """Continue statement"""
    pass

# ============ DECLARATIONS ============

@dataclass
class VariableDeclaration(ASTNode):
    """Variable declaration (e.g., var x = 5)"""
    name: str = ""
    type: Optional[str] = None
    value: Optional[ASTNode] = None

@dataclass
class FunctionDeclaration(ASTNode):
    """Function declaration"""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: ASTNode = None
    return_type: Optional[str] = None

# ============ PINE SCRIPT SPECIFIC ============

@dataclass
class VersionDirective(ASTNode):
    """Pine Script version directive (@version=5)"""
    version: int = 5

@dataclass
class IndicatorDirective(ASTNode):
    """Indicator directive with metadata"""
    title: Optional[str] = None
    short_title: Optional[str] = None
    overlay: bool = False
    scale: Optional[str] = None  # scale.left, scale.right
    precision: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyDirective(ASTNode):
    """Strategy directive with metadata"""
    title: Optional[str] = None
    short_title: Optional[str] = None
    overlay: bool = False
    precision: Optional[int] = None
    currency: Optional[str] = None
    initial_capital: Optional[float] = None
    default_qty_type: Optional[str] = None
    default_qty_value: Optional[float] = None
    commission_type: Optional[str] = None
    commission_value: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlotCall(ASTNode):
    """plot() function call"""
    series: ASTNode = None
    title: Optional[str] = None
    color: Optional[str] = None
    linewidth: Optional[int] = None
    style: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlotShapeCall(ASTNode):
    """plotshape() function call"""
    series: ASTNode = None
    title: Optional[str] = None
    shape: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlotCharCall(ASTNode):
    """plotchar() function call"""
    series: ASTNode = None
    title: Optional[str] = None
    char: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlertCall(ASTNode):
    """alert() function call"""
    message: ASTNode = None
    freq: Optional[str] = None

@dataclass
class StrategyEntryCall(ASTNode):
    """strategy.entry() call"""
    id: ASTNode = None
    direction: ASTNode = None
    qty: Optional[ASTNode] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyExitCall(ASTNode):
    """strategy.exit() call"""
    id: ASTNode = None
    from_entry: Optional[ASTNode] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyCloseCall(ASTNode):
    """strategy.close() call"""
    id: ASTNode = None

@dataclass
class InputCall(ASTNode):
    """input() function call for user inputs"""
    default_value: ASTNode = None
    title: Optional[str] = None
    type: Optional[str] = None
    options: Optional[List[ASTNode]] = None
    extra: Dict[str, Any] = field(default_factory=dict)

# ============ PROGRAM ============

@dataclass
class Program(ASTNode):
    """Root program node - Pine Script complete script"""
    version: Optional[VersionDirective] = None
    directive: Optional[ASTNode] = None  # IndicatorDirective or StrategyDirective
    statements: List[ASTNode] = field(default_factory=list)
    license: Optional[str] = None  # License comment if present
