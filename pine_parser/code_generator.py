"""Code Generator - Generates Python code from Pine Script 6 AST"""

from typing import List, Set, Dict, Optional
from . import ast_nodes as ast


class CodeGenerator:
    """Generates Python code from Pine Script 6 AST"""
    
    def __init__(self):
        self.code_lines: List[str] = []
        self.indent_level = 0
        self.imports: Set[str] = set()
        self.indicator_mapping = self._init_indicator_mapping()
        self.string_methods = self._init_string_methods()
        self.array_methods = self._init_array_methods()
    
    def _init_indicator_mapping(self) -> Dict[str, str]:
        """Map Pine Script indicators to Python implementations"""
        return {
            'ta.sma': 'ta.sma',
            'ta.ema': 'ta.ema',
            'ta.rsi': 'ta.rsi',
            'ta.macd': 'ta.macd',
            'ta.bb': 'ta.bbands',
            'ta.atr': 'ta.atr',
            'ta.stoch': 'ta.stoch',
            'ta.crossover': 'ta.cross',
            'ta.crossunder': 'ta.cross',  # Will handle logic
        }
    
    def _init_string_methods(self) -> Set[str]:
        """String methods available in Pine 6"""
        return {'tostring', 'tonumber', 'contains', 'replace', 'substring', 'upper', 'lower'}
    
    def _init_array_methods(self) -> Set[str]:
        """Array methods available in Pine 6"""
        return {'push', 'pop', 'get', 'set', 'size', 'clear', 'new'}
    
    def generate(self, node: ast.ASTNode) -> str:
        """Generate Python code from AST"""
        self.code_lines = []
        self.indent_level = 0
        self.imports = set()
        
        # Generate code
        self._generate_node(node)
        
        # Collect imports
        import_lines = self._generate_imports()
        
        return import_lines + '\n'.join(self.code_lines)
    
    def _generate_imports(self) -> str:
        """Generate import statements"""
        imports = [
            "import numpy as np",
            "import pandas as pd",
            "import pandas_ta as ta",
            "import backtrader as bt",
        ]
        return '\n'.join(imports) + '\n\n'
    
    def _emit(self, code: str):
        """Emit code line with current indentation"""
        indent = '    ' * self.indent_level
        self.code_lines.append(indent + code)
    
    def _emit_line(self, code: str = ""):
        """Emit code line"""
        if code:
            self._emit(code)
        else:
            self.code_lines.append("")
    
    def _generate_node(self, node: ast.ASTNode) -> str:
        """Generate code from AST node"""
        if node is None:
            return ""
        
        if isinstance(node, ast.Program):
            return self._generate_program(node)
        elif isinstance(node, ast.Block):
            return self._generate_block(node)
        elif isinstance(node, ast.VariableDeclaration):
            return self._generate_variable_declaration(node)
        elif isinstance(node, ast.FunctionDeclaration):
            return self._generate_function_declaration(node)
        elif isinstance(node, ast.IfStatement):
            return self._generate_if_statement(node)
        elif isinstance(node, ast.ForStatement):
            return self._generate_for_statement(node)
        elif isinstance(node, ast.ForInStatement):
            return self._generate_for_in_statement(node)
        elif isinstance(node, ast.WhileStatement):
            return self._generate_while_statement(node)
        elif isinstance(node, ast.BreakStatement):
            return self._generate_break_statement(node)
        elif isinstance(node, ast.ContinueStatement):
            return self._generate_continue_statement(node)
        elif isinstance(node, ast.ReturnStatement):
            return self._generate_return_statement(node)
        elif isinstance(node, ast.Assignment):
            return self._generate_assignment(node)
        elif isinstance(node, ast.BinaryOp):
            return self._generate_binary_op(node)
        elif isinstance(node, ast.UnaryOp):
            return self._generate_unary_op(node)
        elif isinstance(node, ast.TernaryOp):
            return self._generate_ternary_op(node)
        elif isinstance(node, ast.LambdaExpr):
            return self._generate_lambda_expr(node)
        elif isinstance(node, ast.FunctionCall):
            return self._generate_function_call(node)
        elif isinstance(node, ast.MethodCall):
            return self._generate_method_call(node)
        elif isinstance(node, ast.MemberAccess):
            return self._generate_member_access(node)
        elif isinstance(node, ast.ArrayAccess):
            return self._generate_array_access(node)
        elif isinstance(node, ast.Identifier):
            return node.name
        elif isinstance(node, ast.Number):
            return str(node.value)
        elif isinstance(node, ast.String):
            return f"'{node.value}'"
        elif isinstance(node, ast.Boolean):
            return str(node.value)
        elif isinstance(node, ast.NA):
            return "None"
        else:
            return ""
    
    def _generate_program(self, node: ast.Program) -> str:
        """Generate program code"""
        if node.directive:
            if isinstance(node.directive, ast.IndicatorDirective):
                self._generate_indicator_directive(node.directive)
            elif isinstance(node.directive, ast.StrategyDirective):
                self._generate_strategy_directive(node.directive)
            elif isinstance(node.directive, ast.LibraryDirective):
                self._generate_library_directive(node.directive)
            self._emit_line()
        
        for stmt in node.statements:
            self._generate_node(stmt)
        
        return ""
    
    def _generate_indicator_directive(self, node: ast.IndicatorDirective):
        """Generate indicator directive"""
        title = node.title or "Indicator"
        overlay = "True" if node.overlay else "False"
        self._emit_line(f"# @indicator(title='{title}', overlay={overlay})")
    
    def _generate_strategy_directive(self, node: ast.StrategyDirective):
        """Generate strategy directive"""
        title = node.title or "Strategy"
        overlay = "True" if node.overlay else "False"
        self._emit_line(f"# @strategy(title='{title}', overlay={overlay})")
    
    def _generate_library_directive(self, node: ast.LibraryDirective):
        """Generate library directive (Pine 6)"""
        title = node.title or "Library"
        version = node.version or "1.0"
        self._emit_line(f"# @library(title='{title}', version='{version}')")
    
    def _generate_block(self, node: ast.Block) -> str:
        """Generate block code"""
        for stmt in node.statements:
            self._generate_node(stmt)
        return ""
    
    def _generate_variable_declaration(self, node: ast.VariableDeclaration) -> str:
        """Generate variable declaration"""
        if node.value:
            value_code = self._generate_node(node.value)
            self._emit_line(f"{node.name} = {value_code}")
        else:
            self._emit_line(f"{node.name} = None")
        return ""
    
    def _generate_function_declaration(self, node: ast.FunctionDeclaration) -> str:
        """Generate function declaration"""
        params = ', '.join(p.name for p in node.parameters)
        export_prefix = "# @export\n" if node.is_exported else ""
        
        if export_prefix:
            self._emit_line(export_prefix.strip())
        
        self._emit_line(f"def {node.name}({params}):")
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        self._emit_line()
        return ""
    
    def _generate_if_statement(self, node: ast.IfStatement) -> str:
        """Generate if statement"""
        condition = self._generate_node(node.condition)
        self._emit_line(f"if {condition}:")
        
        self.indent_level += 1
        self._generate_node(node.then_body)
        self.indent_level -= 1
        
        if node.else_body:
            self._emit_line("else:")
            self.indent_level += 1
            self._generate_node(node.else_body)
            self.indent_level -= 1
        
        return ""
    
    def _generate_for_statement(self, node: ast.ForStatement) -> str:
        """Generate for loop"""
        if node.init and isinstance(node.init, ast.Assignment):
            init_var = node.init.target
            init_val = self._generate_node(node.init.value)
            self._emit_line(f"{init_var} = {init_val}")
        
        if node.condition:
            condition = self._generate_node(node.condition)
            self._emit_line(f"while {condition}:")
        
            self.indent_level += 1
            self._generate_node(node.body)
            
            if node.update:
                self._generate_node(node.update)
            
            self.indent_level -= 1
        
        return ""
    
    def _generate_for_in_statement(self, node: ast.ForInStatement) -> str:
        """Generate for...in loop (Pine 6)"""
        iterable = self._generate_node(node.iterable)
        self._emit_line(f"for {node.variable} in {iterable}:")
        
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        
        return ""
    
    def _generate_while_statement(self, node: ast.WhileStatement) -> str:
        """Generate while loop"""
        condition = self._generate_node(node.condition)
        self._emit_line(f"while {condition}:")
        
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        
        return ""
    
    def _generate_break_statement(self, node: ast.BreakStatement) -> str:
        """Generate break statement"""
        self._emit_line("break")
        return ""
    
    def _generate_continue_statement(self, node: ast.ContinueStatement) -> str:
        """Generate continue statement"""
        self._emit_line("continue")
        return ""
    
    def _generate_return_statement(self, node: ast.ReturnStatement) -> str:
        """Generate return statement"""
        if node.value:
            value = self._generate_node(node.value)
            self._emit_line(f"return {value}")
        else:
            self._emit_line("return None")
        return ""
    
    def _generate_assignment(self, node: ast.Assignment) -> str:
        """Generate assignment"""
        value = self._generate_node(node.value)
        
        op_map = {
            '=': '=',
            '+=': '+=',
            '-=': '-=',
            '*=': '*=',
            '/=': '/=',
            '%=': '%=',
            '**=': '**=',
        }
        
        op = op_map.get(node.operator, '=')
        self._emit_line(f"{node.target} {op} {value}")
        return ""
    
    def _generate_binary_op(self, node: ast.BinaryOp) -> str:
        """Generate binary operation"""
        left = self._generate_node(node.left)
        right = self._generate_node(node.right)
        
        op_map = {
            'and': 'and',
            'or': 'or',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '**': '**',  # Pine 6 power operator
        }
        
        op = op_map.get(node.operator, node.operator)
        return f"({left} {op} {right})"
    
    def _generate_unary_op(self, node: ast.UnaryOp) -> str:
        """Generate unary operation"""
        operand = self._generate_node(node.operand)
        
        if node.operator == '-':
            return f"(-{operand})"
        elif node.operator in ['not', '!']:
            return f"(not {operand})"
        
        return f"({node.operator}{operand})"
    
    def _generate_ternary_op(self, node: ast.TernaryOp) -> str:
        """Generate ternary operation"""
        condition = self._generate_node(node.condition)
        true_expr = self._generate_node(node.true_expr)
        false_expr = self._generate_node(node.false_expr)
        
        return f"({true_expr} if {condition} else {false_expr})"
    
    def _generate_lambda_expr(self, node: ast.LambdaExpr) -> str:
        """Generate lambda expression (Pine 6)"""
        body = self._generate_node(node.body)
        return f"lambda {node.parameter}: {body}"
    
    def _generate_function_call(self, node: ast.FunctionCall) -> str:
        """Generate function call"""
        args = ', '.join(self._generate_node(arg) for arg in node.arguments)
        
        # Handle special Pine Script functions
        if node.name in self.indicator_mapping:
            return f"{self.indicator_mapping[node.name]}({args})"
        elif node.name.startswith('strategy.'):
            return f"self.{node.name}({args})"
        elif node.name.startswith('request.'):
            return f"request_{node.name.split('.')[1]}({args})"
        else:
            return f"{node.name}({args})"
    
    def _generate_method_call(self, node: ast.MethodCall) -> str:
        """Generate method call"""
        obj = self._generate_node(node.object)
        args = ', '.join(self._generate_node(arg) for arg in node.arguments)
        
        return f"{obj}.{node.method}({args})"
    
    def _generate_member_access(self, node: ast.MemberAccess) -> str:
        """Generate member access"""
        obj = self._generate_node(node.object)
        return f"{obj}.{node.member}"
    
    def _generate_array_access(self, node: ast.ArrayAccess) -> str:
        """Generate array access"""
        array = self._generate_node(node.array)
        index = self._generate_node(node.index)
        return f"{array}[{index}]"
