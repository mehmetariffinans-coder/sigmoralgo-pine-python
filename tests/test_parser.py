"""Test Parser"""

import pytest
from pine_parser import Lexer, Parser
from pine_parser import ast_nodes as ast

def test_parser_variable_declaration():
    """Test parsing variable declaration"""
    code = "var x = 5"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    
    assert isinstance(tree, ast.Program)
    assert len(tree.statements) == 1
    assert isinstance(tree.statements[0], ast.VariableDeclaration)
    assert tree.statements[0].name == "x"

def test_parser_if_statement():
    """Test parsing if statement"""
    code = "if x > 5\nvar y = 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    
    assert isinstance(tree.statements[0], ast.IfStatement)
    assert isinstance(tree.statements[0].condition, ast.BinaryOp)

def test_parser_binary_operation():
    """Test parsing binary operations"""
    code = "var result = 5 + 3 * 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    
    decl = tree.statements[0]
    assert isinstance(decl, ast.VariableDeclaration)
    assert isinstance(decl.value, ast.BinaryOp)

def test_parser_function_call():
    """Test parsing function calls"""
    code = "ta.sma(close, 20)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    
    stmt = tree.statements[0]
    assert isinstance(stmt, ast.MethodCall)
    assert stmt.method == "sma"
