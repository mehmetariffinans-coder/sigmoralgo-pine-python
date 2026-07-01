"""Parser for Pine Script 6 - Builds AST from tokens"""

from typing import List, Optional
from .token_types import Token, TokenType
from . import ast_nodes as ast


class Parser:
    """Parses tokens into an Abstract Syntax Tree"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def error(self, message: str):
        """Raise a parser error"""
        token = self.peek()
        raise SyntaxError(f"Parser error at {token.line}:{token.column}: {message}")
    
    def peek(self, offset: int = 0) -> Token:
        """Peek at token without consuming it"""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        """Consume and return current token"""
        token = self.peek()
        self.position += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume a token of the expected type or raise error"""
        token = self.peek()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return self.advance()
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.peek().type in token_types
    
    def parse(self) -> ast.Program:
        """Parse the token stream into an AST"""
        statements = []
        version = None
        directive = None
        
        self.skip_newlines()
        
        # Parse version directive if present
        if self.peek().type == TokenType.AT and self.peek(1).type == TokenType.IDENTIFIER:
            if self.peek(1).value == 'version':
                version = self.parse_version_directive()
                self.skip_newlines()
        
        # Parse indicator/strategy/library directive
        if self.peek().type == TokenType.INDICATOR:
            directive = self.parse_indicator_directive()
            self.skip_newlines()
        elif self.peek().type == TokenType.STRATEGY:
            directive = self.parse_strategy_directive()
            self.skip_newlines()
        elif self.peek().type == TokenType.LIBRARY:
            directive = self.parse_library_directive()
            self.skip_newlines()
        
        # Parse statements
        while self.peek().type != TokenType.EOF:
            self.skip_newlines()
            
            if self.peek().type == TokenType.EOF:
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            
            self.skip_newlines()
        
        return ast.Program(version=version, directive=directive, statements=statements)
    
    def parse_version_directive(self) -> ast.VersionDirective:
        """Parse @version=N directive"""
        self.expect(TokenType.AT)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        version_token = self.expect(TokenType.NUMBER)
        self.skip_statement_end()
        
        return ast.VersionDirective(
            version=int(float(version_token.value)),
            line=name_token.line,
            column=name_token.column
        )
    
    def parse_indicator_directive(self) -> ast.IndicatorDirective:
        """Parse indicator() directive"""
        indicator_token = self.expect(TokenType.INDICATOR)
        self.expect(TokenType.LPAREN)
        
        kwargs = self.parse_directive_args()
        self.expect(TokenType.RPAREN)
        self.skip_statement_end()
        
        return ast.IndicatorDirective(
            title=kwargs.get('title'),
            short_title=kwargs.get('short_title'),
            overlay=kwargs.get('overlay', False),
            scale=kwargs.get('scale'),
            precision=kwargs.get('precision'),
            timeframe=kwargs.get('timeframe'),
            extra=kwargs,
            line=indicator_token.line,
            column=indicator_token.column
        )
    
    def parse_strategy_directive(self) -> ast.StrategyDirective:
        """Parse strategy() directive"""
        strategy_token = self.expect(TokenType.STRATEGY)
        self.expect(TokenType.LPAREN)
        
        kwargs = self.parse_directive_args()
        self.expect(TokenType.RPAREN)
        self.skip_statement_end()
        
        return ast.StrategyDirective(
            title=kwargs.get('title'),
            short_title=kwargs.get('short_title'),
            overlay=kwargs.get('overlay', False),
            precision=kwargs.get('precision'),
            currency=kwargs.get('currency'),
            initial_capital=kwargs.get('initial_capital'),
            default_qty_type=kwargs.get('default_qty_type'),
            default_qty_value=kwargs.get('default_qty_value'),
            commission_type=kwargs.get('commission_type'),
            commission_value=kwargs.get('commission_value'),
            slippage=kwargs.get('slippage'),
            extra=kwargs,
            line=strategy_token.line,
            column=strategy_token.column
        )
    
    def parse_library_directive(self) -> ast.LibraryDirective:
        """Parse library() directive (Pine 6)"""
        library_token = self.expect(TokenType.LIBRARY)
        self.expect(TokenType.LPAREN)
        
        kwargs = self.parse_directive_args()
        self.expect(TokenType.RPAREN)
        self.skip_statement_end()
        
        return ast.LibraryDirective(
            title=kwargs.get('title'),
            version=kwargs.get('version'),
            extra=kwargs,
            line=library_token.line,
            column=library_token.column
        )
    
    def parse_directive_args(self) -> dict:
        """Parse keyword arguments in directive"""
        kwargs = {}
        
        while not self.match(TokenType.RPAREN) and not self.match(TokenType.EOF):
            key_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.ASSIGN)
            
            # Parse value
            if self.match(TokenType.TRUE):
                self.advance()
                kwargs[key_token.value] = True
            elif self.match(TokenType.FALSE):
                self.advance()
                kwargs[key_token.value] = False
            elif self.match(TokenType.NUMBER):
                num_token = self.advance()
                kwargs[key_token.value] = float(num_token.value)
            elif self.match(TokenType.STRING):
                str_token = self.advance()
                kwargs[key_token.value] = str_token.value
            else:
                self.error("Expected literal value in directive")
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        return kwargs
    
    def parse_statement(self) -> Optional[ast.ASTNode]:
        """Parse a single statement"""
        self.skip_newlines()
        token = self.peek()
        
        if token.type == TokenType.VAR:
            return self.parse_variable_declaration()
        elif token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif token.type == TokenType.BREAK:
            self.advance()
            self.skip_statement_end()
            return ast.BreakStatement(line=token.line, column=token.column)
        elif token.type == TokenType.CONTINUE:
            self.advance()
            self.skip_statement_end()
            return ast.ContinueStatement(line=token.line, column=token.column)
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.LBRACE:
            return self.parse_block()
        elif token.type == TokenType.SEMICOLON:
            self.advance()
            return None
        else:
            return self.parse_expression_statement()
    
    def parse_variable_declaration(self) -> ast.VariableDeclaration:
        """Parse variable declaration: var x = 5 or var x: int = 5"""
        var_token = self.expect(TokenType.VAR)
        name_token = self.expect(TokenType.IDENTIFIER)
        
        var_type = None
        is_varip = False
        
        # Check for type annotation: var x: int = 5
        if self.match(TokenType.COLON):
            self.advance()
            type_token = self.expect(TokenType.IDENTIFIER)
            var_type = type_token.value
        
        value = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
        
        self.skip_statement_end()
        
        return ast.VariableDeclaration(
            name=name_token.value,
            var_type=var_type,
            value=value,
            is_varip=is_varip,
            line=var_token.line,
            column=var_token.column
        )
    
    def parse_function_declaration(self) -> ast.FunctionDeclaration:
        """Parse function declaration with optional return type (Pine 6)"""
        func_token = self.expect(TokenType.FUNCTION)
        name_token = self.expect(TokenType.IDENTIFIER)
        
        self.expect(TokenType.LPAREN)
        parameters = []
        
        while not self.match(TokenType.RPAREN):
            param_token = self.expect(TokenType.IDENTIFIER)
            param_type = None
            default_value = None
            
            # Type annotation: func(x: int, y: float = 1.0)
            if self.match(TokenType.COLON):
                self.advance()
                type_token = self.expect(TokenType.IDENTIFIER)
                param_type = type_token.value
            
            # Default value
            if self.match(TokenType.ASSIGN):
                self.advance()
                default_value = self.parse_expression()
            
            parameters.append(ast.TypedParameter(
                name=param_token.value,
                param_type=param_type or 'unknown',
                default_value=default_value,
                line=param_token.line,
                column=param_token.column
            ))
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        # Return type annotation: func() -> int
        return_type = None
        if self.match(TokenType.ARROW):
            self.advance()
            type_token = self.expect(TokenType.IDENTIFIER)
            return_type = type_token.value
        
        body = self.parse_block()
        
        return ast.FunctionDeclaration(
            name=name_token.value,
            parameters=parameters,
            return_type=return_type,
            body=body,
            line=func_token.line,
            column=func_token.column
        )
    
    def parse_if_statement(self) -> ast.IfStatement:
        """Parse if statement"""
        if_token = self.expect(TokenType.IF)
        condition = self.parse_expression()
        then_body = self.parse_statement()
        
        else_body = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_body = self.parse_statement()
        
        return ast.IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            line=if_token.line,
            column=if_token.column
        )
    
    def parse_for_statement(self) -> ast.ASTNode:
        """Parse for loop (both C-style and for...in - Pine 6)"""
        for_token = self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        
        # Check for for...in pattern
        if self.peek().type == TokenType.IDENTIFIER and self.peek(1).type == TokenType.IN:
            var_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.IN)
            iterable = self.parse_expression()
            self.expect(TokenType.RPAREN)
            body = self.parse_statement()
            
            return ast.ForInStatement(
                variable=var_token.value,
                iterable=iterable,
                body=body,
                line=for_token.line,
                column=for_token.column
            )
        else:
            # C-style for loop
            init = None
            if not self.match(TokenType.SEMICOLON):
                init = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            
            condition = None
            if not self.match(TokenType.SEMICOLON):
                condition = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            
            update = None
            if not self.match(TokenType.RPAREN):
                update = self.parse_expression()
            self.expect(TokenType.RPAREN)
            
            body = self.parse_statement()
            
            return ast.ForStatement(
                init=init,
                condition=condition,
                update=update,
                body=body,
                line=for_token.line,
                column=for_token.column
            )
    
    def parse_while_statement(self) -> ast.WhileStatement:
        """Parse while loop"""
        while_token = self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_statement()
        
        return ast.WhileStatement(
            condition=condition,
            body=body,
            line=while_token.line,
            column=while_token.column
        )
    
    def parse_return_statement(self) -> ast.ReturnStatement:
        """Parse return statement"""
        return_token = self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.EOF):
            value = self.parse_expression()
        
        self.skip_statement_end()
        
        return ast.ReturnStatement(
            value=value,
            line=return_token.line,
            column=return_token.column
        )
    
    def parse_block(self) -> ast.Block:
        """Parse code block { ... }"""
        brace_token = self.expect(TokenType.LBRACE)
        statements = []
        
        self.skip_newlines()
        
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            self.skip_newlines()
            
            if self.match(TokenType.RBRACE):
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return ast.Block(
            statements=statements,
            line=brace_token.line,
            column=brace_token.column
        )
    
    def parse_expression_statement(self) -> Optional[ast.ASTNode]:
        """Parse expression statement"""
        expr = self.parse_expression()
        self.skip_statement_end()
        return expr
    
    def parse_expression(self) -> ast.ASTNode:
        """Parse expression (ternary)"""
        return self.parse_ternary()
    
    def parse_ternary(self) -> ast.ASTNode:
        """Parse ternary expression: a ? b : c"""
        expr = self.parse_or()
        
        if self.match(TokenType.QUESTION):
            self.advance()
            true_expr = self.parse_expression()
            self.expect(TokenType.COLON)
            false_expr = self.parse_expression()
            
            return ast.TernaryOp(
                condition=expr,
                true_expr=true_expr,
                false_expr=false_expr,
                line=expr.line,
                column=expr.column
            )
        
        return expr
    
    def parse_or(self) -> ast.ASTNode:
        """Parse logical OR expression"""
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.parse_and()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_and(self) -> ast.ASTNode:
        """Parse logical AND expression"""
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.parse_equality()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_equality(self) -> ast.ASTNode:
        """Parse equality expression (==, !=)"""
        left = self.parse_relational()
        
        while self.match(TokenType.EQ, TokenType.NE):
            op_token = self.advance()
            right = self.parse_relational()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_relational(self) -> ast.ASTNode:
        """Parse relational expression (<, >, <=, >=)"""
        left = self.parse_additive()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op_token = self.advance()
            right = self.parse_additive()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_additive(self) -> ast.ASTNode:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            right = self.parse_multiplicative()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_multiplicative(self) -> ast.ASTNode:
        """Parse multiplication, division, and modulo"""
        left = self.parse_power()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.parse_power()
            left = ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_power(self) -> ast.ASTNode:
        """Parse power operation (Pine 6: **) - Right-associative"""
        left = self.parse_unary()
        
        if self.match(TokenType.POW):
            op_token = self.advance()
            right = self.parse_power()  # Right-associative
            return ast.BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_unary(self) -> ast.ASTNode:
        """Parse unary expressions (-a, not a)"""
        if self.match(TokenType.MINUS, TokenType.NOT):
            op_token = self.advance()
            operand = self.parse_unary()
            return ast.UnaryOp(
                operator=op_token.value,
                operand=operand,
                line=op_token.line,
                column=op_token.column
            )
        
        return self.parse_lambda()
    
    def parse_lambda(self) -> ast.ASTNode:
        """Parse lambda expression (Pine 6: x => x * 2)"""
        # Look ahead for lambda pattern: identifier => expression
        if self.peek().type == TokenType.IDENTIFIER and self.peek(1).type == TokenType.ARROW:
            param_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.ARROW)
            body = self.parse_additive()
            
            return ast.LambdaExpr(
                parameter=param_token.value,
                body=body,
                line=param_token.line,
                column=param_token.column
            )
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ast.ASTNode:
        """Parse postfix expressions (member access, function call, array access)"""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.DOT):
                self.advance()
                member_token = self.expect(TokenType.IDENTIFIER)
                
                # Method call?
                if self.match(TokenType.LPAREN):
                    self.advance()
                    args = self.parse_arguments()
                    self.expect(TokenType.RPAREN)
                    
                    expr = ast.MethodCall(
                        object=expr,
                        method=member_token.value,
                        arguments=args,
                        line=member_token.line,
                        column=member_token.column
                    )
                else:
                    expr = ast.MemberAccess(
                        object=expr,
                        member=member_token.value,
                        line=member_token.line,
                        column=member_token.column
                    )
            
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                
                expr = ast.ArrayAccess(
                    array=expr,
                    index=index,
                    line=expr.line,
                    column=expr.column
                )
            
            elif self.match(TokenType.LPAREN) and isinstance(expr, ast.Identifier):
                self.advance()
                args = self.parse_arguments()
                self.expect(TokenType.RPAREN)
                
                expr = ast.FunctionCall(
                    name=expr.name,
                    arguments=args,
                    line=expr.line,
                    column=expr.column
                )
            
            else:
                break
        
        # Check for assignment after postfix
        return self.parse_assignment_check(expr)
    
    def parse_assignment_check(self, expr: ast.ASTNode) -> ast.ASTNode:
        """Check for assignment operators after postfix"""
        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                      TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN, TokenType.MOD_ASSIGN,
                      TokenType.POW_ASSIGN):
            
            if not isinstance(expr, ast.Identifier):
                self.error("Invalid assignment target")
            
            op_token = self.advance()
            value = self.parse_expression()
            
            return ast.Assignment(
                target=expr.name,
                value=value,
                operator=op_token.value,
                line=op_token.line,
                column=op_token.column
            )
        
        return expr
    
    def parse_arguments(self) -> List[ast.ASTNode]:
        """Parse function arguments"""
        args = []
        
        while not self.match(TokenType.RPAREN) and not self.match(TokenType.EOF):
            args.append(self.parse_expression())
            
            if self.match(TokenType.COMMA):
                self.advance()
            elif not self.match(TokenType.RPAREN):
                break
        
        return args
    
    def parse_primary(self) -> ast.ASTNode:
        """Parse primary expression"""
        token = self.peek()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return ast.Number(
                value=float(token.value),
                line=token.line,
                column=token.column
            )
        
        elif token.type == TokenType.STRING:
            self.advance()
            return ast.String(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        elif token.type == TokenType.TRUE:
            self.advance()
            return ast.Boolean(
                value=True,
                line=token.line,
                column=token.column
            )
        
        elif token.type == TokenType.FALSE:
            self.advance()
            return ast.Boolean(
                value=False,
                line=token.line,
                column=token.column
            )
        
        elif token.type == TokenType.NA:
            self.advance()
            return ast.NA(line=token.line, column=token.column)
        
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return ast.Identifier(
                name=token.value,
                line=token.line,
                column=token.column
            )
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token: {token.type.name}")
    
    def skip_statement_end(self):
        """Skip semicolon or newline at end of statement"""
        if self.match(TokenType.SEMICOLON):
            self.advance()
        self.skip_newlines()
