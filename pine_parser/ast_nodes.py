"""AST Node definitions for Pine Script"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int = 0

# Literals

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

# Expressions

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
    operator: str = "="  # Can be =, +=, -=, etc.

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

# Statements

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

# Declarations

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

@dataclass
class Program(ASTNode):
    """Root program node"""
    statements: List[ASTNode] = field(default_factory=list)
