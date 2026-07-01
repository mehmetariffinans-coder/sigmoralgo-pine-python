"""Enhanced Lexer for Pine Script with TradingView support"""

import re
from typing import List, Optional
from .token_types import Token, TokenType, KEYWORDS, BUILTIN_SERIES

class Lexer:
    """Tokenizes Pine Script code into tokens"""
    
    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """Raise a lexer error"""
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Peek at character without consuming it"""
        pos = self.position + offset
        if pos < len(self.code):
            return self.code[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return next character"""
        if self.position < len(self.code):
            char = self.code[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        """Skip whitespace but not newlines"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_license_comment(self):
        """Skip license header comments at start of file"""
        if self.peek() == '/' and self.peek(1) == '/':
            # Check if it contains "This Pine Script" or "Mozilla Public License"
            start_pos = self.position
            line_content = ''
            while self.peek() and self.peek() != '\n':
                line_content += self.peek()
                self.advance()
            
            if 'This Pine Script' in line_content or 'Mozilla' in line_content or '©' in line_content:
                if self.peek() == '\n':
                    self.advance()
                return True
            else:
                # Not a license comment, restore position
                self.position = start_pos
                self.column -= len(line_content)
        
        return False
    
    def skip_comment(self):
        """Skip single-line or multi-line comments"""
        if self.peek() == '/' and self.peek(1) == '/':
            # Single-line comment
            while self.peek() and self.peek() != '\n':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            # Multi-line comment
            self.advance()  # /
            self.advance()  # *
            while self.position < len(self.code) - 1:
                if self.peek() == '*' and self.peek(1) == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number token"""
        start_line = self.line
        start_column = self.column
        number_str = ''
        
        # Handle hex (0x) or binary (0b)
        if self.peek() == '0' and self.peek(1) in 'xXbB':
            number_str += self.advance()  # 0
            number_str += self.advance()  # x or b
            while self.peek() and self.peek() in '0123456789abcdefABCDEF':
                number_str += self.advance()
        else:
            # Regular decimal
            while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
                number_str += self.advance()
        
        return Token(TokenType.NUMBER, number_str, start_line, start_column)
    
    def read_string(self, quote: str) -> Token:
        """Read a string token"""
        start_line = self.line
        start_column = self.column
        string_val = ''
        
        self.advance()  # Skip opening quote
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                escaped = self.advance()
                if escaped == 'n':
                    string_val += '\n'
                elif escaped == 't':
                    string_val += '\t'
                elif escaped == 'r':
                    string_val += '\r'
                elif escaped == '\\':
                    string_val += '\\'
                elif escaped == quote:
                    string_val += quote
                else:
                    string_val += escaped
            else:
                string_val += self.advance()
        
        if self.peek() != quote:
            self.error(f"Unterminated string starting at {start_line}:{start_column}")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_val, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword token"""
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() in '_'):
            identifier += self.advance()
        
        # Check if it's a keyword or built-in series
        token_type = KEYWORDS.get(identifier.lower(), TokenType.IDENTIFIER)
        
        return Token(token_type, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the input code"""
        self.tokens = []
        
        # Skip license comments at start of file
        while self.skip_license_comment():
            pass
        
        while self.position < len(self.code):
            self.skip_whitespace()
            
            # Skip comments
            if self.peek() == '/' and self.peek(1) in '/*':
                self.skip_comment()
                continue
            
            char = self.peek()
            
            if char is None:
                break
            
            line = self.line
            column = self.column
            
            # Newline
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char in '\\"\'':
                self.tokens.append(self.read_string(char))
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', line, column))
                else:
                    self.tokens.append(Token(TokenType.PLUS, '+', line, column))
            
            elif char == '-':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', line, column))
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', line, column))
            
            elif char == '*':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.STAR_ASSIGN, '*=', line, column))
                else:
                    self.tokens.append(Token(TokenType.STAR, '*', line, column))
            
            elif char == '/':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.SLASH_ASSIGN, '/=', line, column))
                else:
                    self.tokens.append(Token(TokenType.SLASH, '/', line, column))
            
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.PERCENT, '%', line, column))
            
            elif char == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', line, column))
                elif self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, '=>', line, column))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', line, column))
            
            elif char == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, '!=', line, column))
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', line, column))
            
            elif char == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LE, '<=', line, column))
                else:
                    self.tokens.append(Token(TokenType.LT, '<', line, column))
            
            elif char == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GE, '>=', line, column))
                else:
                    self.tokens.append(Token(TokenType.GT, '>', line, column))
            
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, column))
            
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, column))
            
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', line, column))
            
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', line, column))
            
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', line, column))
            
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', line, column))
            
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, column))
            
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', line, column))
            
            elif char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.QUESTION, '?', line, column))
            
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', line, column))
            
            elif char == '@':
                self.advance()
                self.tokens.append(Token(TokenType.AT, '@', line, column))
            
            else:
                self.error(f"Unexpected character: {char!r}")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
