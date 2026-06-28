"""Parser for Pine Script - Builds AST from tokens"""

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
        
        self.skip_newlines()
        
        while self.peek().type != TokenType.EOF:
            self.skip_newlines()
            
            if self.peek().type == TokenType.EOF:
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            
            self.skip_newlines()
        
        return ast.Program(statements=statements)
    
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
        """Parse variable declaration: var x = 5"""
        var_token = self.expect(TokenType.VAR)
        name_token = self.expect(TokenType.IDENTIFIER)
        
        value = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
        
        self.skip_statement_end()
        
        return ast.VariableDeclaration(
            name=name_token.value,
            value=value,
            line=var_token.line,
            column=var_token.column
        )
    
    def parse_function_declaration(self) -> ast.FunctionDeclaration:
        """Parse function declaration"""
        func_token = self.expect(TokenType.FUNCTION)
        name_token = self.expect(TokenType.IDENTIFIER)
        
        self.expect(TokenType.LPAREN)
        parameters = []
        
        while not self.match(TokenType.RPAREN):
            param = self.expect(TokenType.IDENTIFIER)
            parameters.append(param.value)
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block()
        
        return ast.FunctionDeclaration(
            name=name_token.value,
            parameters=parameters,
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
    
    def parse_for_statement(self) -> ast.ForStatement:
        """Parse for loop"""
        for_token = self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        
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
        left = self.parse_unary()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.parse_unary()
            left = ast.BinaryOp(
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
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ast.ASTNode:
        """Parse postfix expressions (member access, function call, array access)"""
        expr = self.parse_assignment()
        
        while True:
            if self.match(TokenType.DOT):
                self.advance()
                member_token = self.expect(TokenType.IDENTIFIER)
                
                # Check if it's a method call
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
                # Function call
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
        
        return expr
    
    def parse_assignment(self) -> ast.ASTNode:
        """Parse assignment expression"""
        expr = self.parse_primary()
        
        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                      TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN):
            
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
