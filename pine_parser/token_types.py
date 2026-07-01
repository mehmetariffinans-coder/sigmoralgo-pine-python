"""Token types for Pine Script 6 Lexer with full TradingView support"""

from enum import Enum, auto

class TokenType(Enum):
    """Token types for Pine Script 6"""
    
    # ===== LITERALS =====
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    NA = auto()
    
    # ===== KEYWORDS (CONTROL FLOW) =====
    VAR = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()           # Pine 6: for...in loops
    WHILE = auto()
    BREAK = auto()        # Pine 6: break
    CONTINUE = auto()     # Pine 6: continue
    RETURN = auto()
    
    # ===== KEYWORDS (DECLARATIONS) =====
    FUNCTION = auto()
    IMPORT = auto()
    EXPORT = auto()       # Pine 6: @export decorator
    TYPE = auto()         # Pine 6: custom types
    
    # ===== KEYWORDS (TYPE ANNOTATIONS) =====
    INT_TYPE = auto()     # int
    FLOAT_TYPE = auto()   # float
    BOOL_TYPE = auto()    # bool
    STRING_TYPE = auto()  # string
    ARRAY = auto()        # Pine 6: array<T>
    MAP = auto()          # Pine 6: map<K,V>
    MATRIX = auto()       # Pine 6: matrix<T>
    
    # ===== PINE SCRIPT DIRECTIVES =====
    INDICATOR = auto()
    STRATEGY = auto()
    LIBRARY = auto()      # Pine 6: library
    PLOT = auto()
    PLOTSHAPE = auto()
    PLOTCHAR = auto()
    ALERT = auto()
    INPUT = auto()
    HLINE = auto()
    FILL = auto()
    
    # ===== OPERATORS (ARITHMETIC) =====
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # /
    PERCENT = auto()      # %
    POW = auto()          # ** (Pine 6)
    
    # ===== OPERATORS (COMPARISON) =====
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=
    
    # ===== OPERATORS (LOGICAL) =====
    AND = auto()          # and
    OR = auto()           # or
    NOT = auto()          # not
    
    # ===== OPERATORS (ASSIGNMENT) =====
    ASSIGN = auto()       # =
    PLUS_ASSIGN = auto()  # +=
    MINUS_ASSIGN = auto() # -=
    STAR_ASSIGN = auto()  # *=
    SLASH_ASSIGN = auto() # /=
    MOD_ASSIGN = auto()   # %= (Pine 6)
    POW_ASSIGN = auto()   # **= (Pine 6)
    
    # ===== OPERATORS (SPECIAL) =====
    QUESTION = auto()     # ?
    COLON = auto()        # :
    ARROW = auto()        # => (Pine 6: lambda)
    AT = auto()           # @ (decorators)
    COLON_COLON = auto()  # :: (namespace) - Pine 6
    
    # ===== DELIMITERS =====
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,
    DOT = auto()          # .
    NEWLINE = auto()
    
    # ===== SPECIAL =====
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


# Keywords mapping (Pine Script 6)
KEYWORDS = {
    # Control flow
    'var': TokenType.VAR,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'while': TokenType.WHILE,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'return': TokenType.RETURN,
    
    # Declarations
    'function': TokenType.FUNCTION,
    'import': TokenType.IMPORT,
    'export': TokenType.EXPORT,
    'type': TokenType.TYPE,
    
    # Types
    'int': TokenType.INT_TYPE,
    'float': TokenType.FLOAT_TYPE,
    'bool': TokenType.BOOL_TYPE,
    'string': TokenType.STRING_TYPE,
    'array': TokenType.ARRAY,
    'map': TokenType.MAP,
    'matrix': TokenType.MATRIX,
    
    # Directives
    'indicator': TokenType.INDICATOR,
    'strategy': TokenType.STRATEGY,
    'library': TokenType.LIBRARY,
    'plot': TokenType.PLOT,
    'plotshape': TokenType.PLOTSHAPE,
    'plotchar': TokenType.PLOTCHAR,
    'alert': TokenType.ALERT,
    'input': TokenType.INPUT,
    'hline': TokenType.HLINE,
    'fill': TokenType.FILL,
    
    # Literals
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'na': TokenType.NA,
    
    # Logical
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
}

# Built-in Pine Script series
BUILTIN_SERIES = {
    'close', 'open', 'high', 'low', 'volume',
    'hl2', 'hlc3', 'ohlc4',
    'time', 'bar_index', 'bar_time',
}

# Pine Script built-in namespaces and functions (Pine 6)
BUILTIN_FUNCTIONS = {
    # Technical Analysis (ta.*)
    'ta.sma', 'ta.ema', 'ta.rsi', 'ta.macd', 'ta.bb',
    'ta.atr', 'ta.stoch', 'ta.roc', 'ta.momentum',
    'ta.crossover', 'ta.crossunder',
    
    # Math
    'math.abs', 'math.sqrt', 'math.pow', 'math.log',
    'math.sin', 'math.cos', 'math.tan', 'math.min', 'math.max',
    
    # String (Pine 6)
    'str.tostring', 'str.tonumber', 'str.contains',
    'str.replace', 'str.substring', 'str.upper', 'str.lower',
    
    # Array (Pine 6)
    'array.new', 'array.push', 'array.pop', 'array.get', 'array.set',
    'array.size', 'array.clear', 'array.slice',
    
    # Map (Pine 6)
    'map.new', 'map.put', 'map.get', 'map.remove', 'map.keys',
    
    # Strategy
    'strategy.entry', 'strategy.exit', 'strategy.close',
    'strategy.order', 'strategy.cancel',
    
    # Chart/Request (Pine 6)
    'request.security', 'request.quandl', 'request.dividends',
    'request.earnings', 'request.splits',
    
    # Utilities
    'print', 'len', 'typeof',
}
