"""Semantic Analyzer for Pine Script 6 - Type checking and validation"""

from typing import Dict, Optional, Set, List, Tuple
from . import ast_nodes as ast


class SemanticAnalyzer:
    """Analyzes AST for semantic correctness and type safety (Pine 6)"""
    
    def __init__(self):
        self.variables: Dict[str, str] = {}  # name -> type
        self.functions: Dict[str, Tuple[List, str]] = {}  # name -> (params, return_type)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.builtin_functions = self._init_builtin_functions()
    
    def _init_builtin_functions(self) -> Dict[str, Tuple[List[str], str]]:
        """Initialize built-in Pine Script 6 functions"""
        return {
            # Technical Analysis (ta.*)
            'ta.sma': (['series', 'length'], 'float'),
            'ta.ema': (['series', 'length'], 'float'),
            'ta.rsi': (['series', 'length'], 'float'),
            'ta.macd': (['series', 'fast', 'slow'], 'tuple'),
            'ta.bb': (['series', 'length', 'stddev'], 'tuple'),
            'ta.atr': (['length'], 'float'),
            'ta.stoch': (['high', 'low', 'close', 'k', 'd'], 'tuple'),
            'ta.crossover': (['a', 'b'], 'bool'),
            'ta.crossunder': (['a', 'b'], 'bool'),
            
            # Math
            'math.abs': (['x'], 'float'),
            'math.sqrt': (['x'], 'float'),
            'math.pow': (['x', 'y'], 'float'),
            'math.log': (['x'], 'float'),
            'math.sin': (['x'], 'float'),
            'math.cos': (['x'], 'float'),
            'math.tan': (['x'], 'float'),
            'math.min': (['a', 'b'], 'float'),
            'math.max': (['a', 'b'], 'float'),
            
            # String (Pine 6)
            'str.tostring': (['value'], 'string'),
            'str.tonumber': (['value'], 'float'),
            'str.contains': (['text', 'substring'], 'bool'),
            'str.replace': (['text', 'old', 'new'], 'string'),
            'str.substring': (['text', 'start', 'end'], 'string'),
            'str.upper': (['text'], 'string'),
            'str.lower': (['text'], 'string'),
            
            # Array (Pine 6)
            'array.new': (['type'], 'array'),
            'array.push': (['array', 'value'], 'void'),
            'array.pop': (['array'], 'unknown'),
            'array.get': (['array', 'index'], 'unknown'),
            'array.set': (['array', 'index', 'value'], 'void'),
            'array.size': (['array'], 'int'),
            'array.clear': (['array'], 'void'),
            
            # Strategy
            'strategy.entry': (['id', 'direction', 'qty'], 'void'),
            'strategy.exit': (['id'], 'void'),
            'strategy.close': (['id'], 'void'),
            'strategy.order': (['id', 'direction', 'qty'], 'void'),
            'strategy.cancel': (['id'], 'void'),
            
            # Request (Pine 6)
            'request.security': (['symbol', 'timeframe', 'expression'], 'float'),
            'request.quandl': (['ticker', 'period'], 'float'),
            
            # Plot
            'plot': (['series'], 'void'),
            'hline': (['price'], 'void'),
            'fill': (['series1', 'series2'], 'void'),
            'plotshape': (['series'], 'void'),
            'plotchar': (['series'], 'void'),
            
            # Utilities
            'print': (['message'], 'void'),
            'len': (['obj'], 'int'),
            'typeof': (['value'], 'string'),
            'alert': (['message'], 'void'),
            'input': (['default'], 'unknown'),
        }
    
    def analyze(self, node: ast.ASTNode) -> bool:
        """Analyze AST node and return True if no errors found"""
        self.errors = []
        self.warnings = []
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
        elif isinstance(node, ast.ForInStatement):
            self._analyze_for_in_statement(node)
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
        elif isinstance(node, ast.LambdaExpr):
            self._analyze_lambda_expr(node)
    
    def _analyze_program(self, node: ast.Program):
        """Analyze program node"""
        if node.directive:
            self._analyze_node(node.directive)
        
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
        
        # Determine variable type
        var_type = node.var_type or 'unknown'
        if not node.var_type and node.value:
            var_type = self._infer_type(node.value)
        
        self.variables[node.name] = var_type
    
    def _analyze_function_declaration(self, node: ast.FunctionDeclaration):
        """Analyze function declaration"""
        param_types = [p.param_type or 'unknown' for p in node.parameters]
        self.functions[node.name] = (param_types, node.return_type or 'unknown')
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
    
    def _analyze_for_in_statement(self, node: ast.ForInStatement):
        """Analyze for...in loop (Pine 6)"""
        self._analyze_node(node.iterable)
        # Add loop variable to scope
        self.variables[node.variable] = 'unknown'
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
            self.warnings.append(
                f"Unknown function '{node.name}' at line {node.line}"
            )
        
        for arg in node.arguments:
            self._analyze_node(arg)
    
    def _analyze_method_call(self, node: ast.MethodCall):
        """Analyze method call"""
        self._analyze_node(node.object)
        
        for arg in node.arguments:
            self._analyze_node(arg)
    
    def _analyze_lambda_expr(self, node: ast.LambdaExpr):
        """Analyze lambda expression (Pine 6)"""
        self.variables[node.parameter] = 'unknown'
        self._analyze_node(node.body)
    
    def _infer_type(self, node: ast.ASTNode) -> str:
        """Infer type from expression (Pine 6)"""
        if isinstance(node, ast.Number):
            return 'float'
        elif isinstance(node, ast.String):
            return 'string'
        elif isinstance(node, ast.Boolean):
            return 'bool'
        elif isinstance(node, ast.NA):
            return 'na'
        elif isinstance(node, ast.ArrayDeclaration):
            return 'array'
        elif isinstance(node, ast.MapDeclaration):
            return 'map'
        elif isinstance(node, ast.MatrixDeclaration):
            return 'matrix'
        elif isinstance(node, ast.LambdaExpr):
            return 'function'
        else:
            return 'unknown'
    
    def get_errors(self) -> List[str]:
        """Get all collected errors"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get all collected warnings"""
        return self.warnings
