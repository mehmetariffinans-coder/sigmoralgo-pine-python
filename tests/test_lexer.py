"""Tests for Pine Script 6 Lexer"""

import pytest
from pine_parser.lexer import Lexer
from pine_parser.token_types import TokenType


class TestLexerBasic:
    """Test basic lexer functionality"""
    
    def test_tokenize_simple_number(self):
        """Test number tokenization"""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "42"
    
    def test_tokenize_float(self):
        """Test float tokenization"""
        lexer = Lexer("3.14")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "3.14"
    
    def test_tokenize_string(self):
        """Test string tokenization"""
        lexer = Lexer('"hello world"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello world"
    
    def test_tokenize_identifier(self):
        """Test identifier tokenization"""
        lexer = Lexer("myVariable")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "myVariable"
    
    def test_tokenize_keyword(self):
        """Test keyword tokenization"""
        lexer = Lexer("var x = 5")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.VAR
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[2].type == TokenType.ASSIGN
        assert tokens[3].type == TokenType.NUMBER


class TestLexerOperators:
    """Test operator tokenization"""
    
    def test_power_operator(self):
        """Test ** power operator (Pine 6)"""
        lexer = Lexer("a ** b")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.POW
        assert tokens[1].value == "**"
    
    def test_power_assign(self):
        """Test **= power assignment (Pine 6)"""
        lexer = Lexer("a **= b")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.POW_ASSIGN
        assert tokens[1].value == "**="
    
    def test_mod_assign(self):
        """Test %= modulo assignment (Pine 6)"""
        lexer = Lexer("a %= b")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.MOD_ASSIGN
        assert tokens[1].value == "%="
    
    def test_lambda_arrow(self):
        """Test => lambda arrow (Pine 6)"""
        lexer = Lexer("x => x * 2")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.ARROW
        assert tokens[1].value == "=>"
    
    def test_namespace_operator(self):
        """Test :: namespace operator (Pine 6)"""
        lexer = Lexer("a :: b")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.COLON_COLON
        assert tokens[1].value == "::"


class TestLexerComments:
    """Test comment handling"""
    
    def test_single_line_comment(self):
        """Test single-line comment"""
        lexer = Lexer("// This is a comment\nx = 5")
        tokens = lexer.tokenize()
        # Comment should be skipped
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
    
    def test_multi_line_comment(self):
        """Test multi-line comment"""
        lexer = Lexer("/* comment */ x = 5")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"


class TestLexerPine6Keywords:
    """Test Pine 6 keywords"""
    
    def test_for_in_keyword(self):
        """Test for...in keywords (Pine 6)"""
        lexer = Lexer("for x in arr")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FOR
        assert tokens[2].type == TokenType.IN
    
    def test_break_continue(self):
        """Test break and continue (Pine 6)"""
        lexer = Lexer("break continue")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.BREAK
        assert tokens[1].type == TokenType.CONTINUE
    
    def test_type_keywords(self):
        """Test type keywords (Pine 6)"""
        lexer = Lexer("int float bool string array map matrix")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INT_TYPE
        assert tokens[1].type == TokenType.FLOAT_TYPE
        assert tokens[2].type == TokenType.BOOL_TYPE
        assert tokens[3].type == TokenType.STRING_TYPE
        assert tokens[4].type == TokenType.ARRAY
        assert tokens[5].type == TokenType.MAP
        assert tokens[6].type == TokenType.MATRIX
