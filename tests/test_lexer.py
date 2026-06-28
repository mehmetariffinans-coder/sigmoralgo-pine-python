"""Test Lexer"""

import pytest
from pine_parser import Lexer
from pine_parser.token_types import TokenType

def test_lexer_numbers():
    """Test number tokenization"""
    code = "123 45.67 0xff 0b1010"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "45.67"

def test_lexer_keywords():
    """Test keyword tokenization"""
    code = "var if else for while"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.VAR
    assert tokens[1].type == TokenType.IF
    assert tokens[2].type == TokenType.ELSE
    assert tokens[3].type == TokenType.FOR
    assert tokens[4].type == TokenType.WHILE

def test_lexer_operators():
    """Test operator tokenization"""
    code = "+ - * / == != < > <= >= and or"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.PLUS
    assert tokens[1].type == TokenType.MINUS
    assert tokens[2].type == TokenType.STAR
    assert tokens[3].type == TokenType.SLASH
    assert tokens[4].type == TokenType.EQ
    assert tokens[5].type == TokenType.NE

def test_lexer_strings():
    """Test string tokenization"""
    code = '"hello" \'world\''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "world"

def test_lexer_comments():
    """Test comment skipping"""
    code = "x = 5 // comment\ny = 10 /* block comment */ z = 15"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Comments should be skipped
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
