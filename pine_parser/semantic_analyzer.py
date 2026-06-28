"""Semantic Analyzer - Type checking and validation"""

from typing import Dict, Optional, Set
from . import ast_nodes as ast

class SemanticAnalyzer:
    """Analyzes AST for semantic correctness"""
    
    def __init__(self):
        self.variables: Dict[str, str] = {}  # name -> type
        self.functions: Dict[str, tuple] = {}  # name -> (params, return_type)
        self.errors: list = []
        self.builtin_functions = self._init_builtin_functions()
    
    def _init_builtin_functions(self) -> Dict[str, tuple]:
        """Initialize built-in Pine Script functions"""
        return {
            # Technical Analysis
            'ta.sma': (['series', 'length'], 'float'),
            'ta.ema': (['series', 'length'], 'float'),
            'ta.rsi': (['series', 'length'], 'float'),
            'ta.macd': (['series', 'fast', 'slow'], 'tuple'),
            'ta.bb': (['series', 'length', 'stddev'], 'tuple'),
            'ta.atr': (['length'], 'float'),
            'ta.stoch': (['high', 'low', 'close', 'k', 'd'], 'tuple'),
            
            # Math
            'math.abs': (['x'], 'float'),
            'math.sqrt': (['x'], 'float'),
            'math.pow': (['x', 'y'], 'float'),
            'math.log': (['x'], 'float'),
            'math.sin': (['x'], 'float'),
            'math.cos': (['x'], 'float'),
            'math.min': (['a', 'b'], 'float'),
            'math.max': (['a', 'b'], 'float'),
            
            # Strategy
            'strategy.entry': (['id', 'direction', 'qty'], 'void'),
            'strategy.exit': (['id'], 'void'),
            'strategy.close': (['id'], 'void'),
            'strategy.order': (['id', 'direction', 'qty'], 'void'),
            
            # Data
            'request.security': (['symbol', 'timeframe', 'expression'], 'float'),
            
            # Utilities
            'print': (['message'], 'void'),
            'len': (['obj'], 'int'),
        }
    
    def analyze(self, node: ast.ASTNode) -> bool:
        """Analyze AST node and return True if no errors found"""
        self.errors = []
        self._analyze_node(node)
        return len(self.errors) == 0
    
    def _analyze_node(self, node: ast.ASTNode):
        """Recursively analyze AST node"""
        if node is None:
            return
        
        if isinstance(node, ast.Program):
            self._analyze_program(node)
        elif isinstance(node, ast.VariableDeclaration):
            self._analyze_variable_declaration(node)
        elif isinstance(node, ast.FunctionDeclaration):
            self._analyze_function_declaration(node)
        elif isinstance(node, ast.Block):
            self._analyze_block(node)
        elif isinstance(node, ast.IfStatement):
            self._analyze_if_statement(node)
        elif isinstance(node, ast.ForStatement):
            self._analyze_for_statement(node)
        elif isinstance(node, ast.WhileStatement):
            self._analyze_while_statement(node)
        elif isinstance(node, ast.Assignment):
            self._analyze_assignment(node)
        elif isinstance(node, ast.BinaryOp):
            self._analyze_binary_op(node)
        elif isinstance(node, ast.FunctionCall):
            self._analyze_function_call(node)
        elif isinstance(node, ast.MethodCall):
            self._analyze_method_call(node)
    
    def _analyze_program(self, node: ast.Program):
        """Analyze program node"""
        for stmt in node.statements:
            self._analyze_node(stmt)
    
    def _analyze_variable_declaration(self, node: ast.VariableDeclaration):
        """Analyze variable declaration"""
        if node.name in self.variables:
            self.errors.append(
                f"Variable '{node.name}' already declared at line {node.line}"
            )
        
        if node.value:
            self._analyze_node(node.value)
        
        # Infer type from value
        var_type = 'unknown'
        if isinstance(node.value, ast.Number):
            var_type = 'float'
        elif isinstance(node.value, ast.String):
            var_type = 'string'
        elif isinstance(node.value, ast.Boolean):
            var_type = 'bool'
        elif isinstance(node.value, ast.NA):
            var_type = 'na'
        
        self.variables[node.name] = var_type
    
    def _analyze_function_declaration(self, node: ast.FunctionDeclaration):
        """Analyze function declaration"""
        self.functions[node.name] = (node.parameters, node.return_type or 'unknown')
        self._analyze_node(node.body)
    
    def _analyze_block(self, node: ast.Block):
        """Analyze code block"""
        for stmt in node.statements:
            self._analyze_node(stmt)
    
    def _analyze_if_statement(self, node: ast.IfStatement):
        """Analyze if statement"""
        self._analyze_node(node.condition)
        self._analyze_node(node.then_body)
        if node.else_body:
            self._analyze_node(node.else_body)
    
    def _analyze_for_statement(self, node: ast.ForStatement):
        """Analyze for loop"""
        if node.init:
            self._analyze_node(node.init)
        if node.condition:
            self._analyze_node(node.condition)
        if node.update:
            self._analyze_node(node.update)
        self._analyze_node(node.body)
    
    def _analyze_while_statement(self, node: ast.WhileStatement):
        """Analyze while loop"""
        self._analyze_node(node.condition)
        self._analyze_node(node.body)
    
    def _analyze_assignment(self, node: ast.Assignment):
        """Analyze assignment"""
        if node.target not in self.variables:
            # Implicit declaration
            self.variables[node.target] = 'unknown'
        
        self._analyze_node(node.value)
    
    def _analyze_binary_op(self, node: ast.BinaryOp):
        """Analyze binary operation"""
        self._analyze_node(node.left)
        self._analyze_node(node.right)
    
    def _analyze_function_call(self, node: ast.FunctionCall):
        """Analyze function call"""
        if node.name not in self.builtin_functions and node.name not in self.functions:
            self.errors.append(
                f"Unknown function '{node.name}' at line {node.line}"
            )
        
        for arg in node.arguments:
            self._analyze_node(arg)
    
    def _analyze_method_call(self, node: ast.MethodCall):
        """Analyze method call"""
        self._analyze_node(node.object)
        
        for arg in node.arguments:
            self._analyze_node(arg)
    
    def get_errors(self) -> list:
        """Get all collected errors"""
        return self.errors
