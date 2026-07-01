"""Token types for Pine Script lexer with TradingView support"""

from enum import Enum, auto

class TokenType(Enum):
    """Token types"""
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    NA = auto()
    
    # Keywords
    VAR = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    FUNCTION = auto()
    RETURN = auto()
    IMPORT = auto()
    
    # Pine Script Keywords
    INDICATOR = auto()
    STRATEGY = auto()
    PLOT = auto()
    PLOTSHAPE = auto()
    PLOTCHAR = auto()
    ALERT = auto()
    INPUT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()
    
    # Comparison
    EQ = auto()      # ==
    NE = auto()      # !=
    LT = auto()      # <
    LE = auto()      # <=
    GT = auto()      # >
    GE = auto()      # >=
    
    # Logical
    AND = auto()     # and
    OR = auto()      # or
    NOT = auto()     # not
    
    # Assignment
    ASSIGN = auto()  # =
    PLUS_ASSIGN = auto()   # +=
    MINUS_ASSIGN = auto()  # -=
    STAR_ASSIGN = auto()   # *=
    SLASH_ASSIGN = auto()  # /=
    
    # Ternary
    QUESTION = auto()  # ?
    COLON = auto()     # :
    
    # Delimiters
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LBRACE = auto()    # {
    RBRACE = auto()    # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    SEMICOLON = auto() # ;
    COMMA = auto()     # ,
    DOT = auto()       # .
    ARROW = auto()     # =>
    AT = auto()        # @
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    ERROR = auto()

class Token:
    """Represents a single token"""
    
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"

# Keywords mapping
KEYWORDS = {
    'var': TokenType.VAR,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'for': TokenType.FOR,
    'while': TokenType.WHILE,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'import': TokenType.IMPORT,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'na': TokenType.NA,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'indicator': TokenType.INDICATOR,
    'strategy': TokenType.STRATEGY,
    'plot': TokenType.PLOT,
    'plotshape': TokenType.PLOTSHAPE,
    'plotchar': TokenType.PLOTCHAR,
    'alert': TokenType.ALERT,
    'input': TokenType.INPUT,
}

# Pine Script built-in series
BUILTIN_SERIES = {
    'close', 'open', 'high', 'low', 'volume',
    'hl2', 'hlc3', 'ohlc4',
    'time', 'bar_index', 'bar_time',
}
