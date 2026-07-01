"""Main Pine Script to Python Converter with TradingView support"""

from pine_parser import Lexer, Parser, CodeGenerator, SemanticAnalyzer

class PineScriptConverter:
    """Main converter class for Pine Script to Python"""
    
    def __init__(self):
        self.errors = []
    
    def convert(self, pine_code: str) -> str:
        """Convert Pine Script code to Python
        
        Args:
            pine_code: Pine Script source code (including TradingView directives)
        
        Returns:
            Python source code
        
        Raises:
            SyntaxError: If there are syntax errors in the input
        
        Example:
            >>> code = '''
            ... //@version=6
            ... indicator("My Indicator")
            ... plot(close)
            ... '''
            >>> converter = PineScriptConverter()
            >>> python_code = converter.convert(code)
        """
        self.errors = []
        
        # Stage 1: Lexical Analysis
        try:
            lexer = Lexer(pine_code)
            tokens = lexer.tokenize()
        except SyntaxError as e:
            self.errors.append(f"Lexer error: {e}")
            raise
        
        # Stage 2: Parsing
        try:
            parser = Parser(tokens)
            ast = parser.parse()
        except SyntaxError as e:
            self.errors.append(f"Parser error: {e}")
            raise
        
        # Stage 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        if not analyzer.analyze(ast):
            self.errors.extend(analyzer.get_errors())
            print("\nSemantic warnings (not fatal):")
            for error in analyzer.get_errors():
                print(f"  - {error}")
        
        # Stage 4: Code Generation
        generator = CodeGenerator()
        python_code = generator.generate(ast)
        
        return python_code
    
    def convert_file(self, filename: str) -> str:
        """Convert Pine Script file to Python
        
        Args:
            filename: Path to Pine Script file
        
        Returns:
            Python source code
        """
        with open(filename, 'r', encoding='utf-8') as f:
            pine_code = f.read()
        
        return self.convert(pine_code)
    
    def convert_to_file(self, pine_code: str, output_filename: str):
        """Convert Pine Script to Python file
        
        Args:
            pine_code: Pine Script source code
            output_filename: Path to output Python file
        """
        python_code = self.convert(pine_code)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(python_code)
    
    def get_errors(self) -> list:
        """Get list of errors from last conversion"""
        return self.errors


if __name__ == "__main__":
    # Example 1: Simple indicator with plot
    pine_code_1 = """
    //@version=6
    indicator("Komut dosyam")
    plot(close)
    """
    
    print("=" * 60)
    print("EXAMPLE 1: Simple Indicator")
    print("=" * 60)
    print("\nPine Script Input:")
    print(pine_code_1)
    
    converter = PineScriptConverter()
    try:
        python_code = converter.convert(pine_code_1)
        print("\nGenerated Python Code:")
        print(python_code)
    except SyntaxError as e:
        print(f"Error: {e}")
    
    # Example 2: Indicator with SMA
    pine_code_2 = """
    //@version=6
    indicator("SMA Indicator", overlay=true)
    ma = ta.sma(close, 20)
    plot(ma, color=color.red)
    """
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: SMA Indicator")
    print("=" * 60)
    print("\nPine Script Input:")
    print(pine_code_2)
    
    try:
        python_code = converter.convert(pine_code_2)
        print("\nGenerated Python Code:")
        print(python_code)
    except SyntaxError as e:
        print(f"Error: {e}")
    
    # Example 3: Complex indicator with conditions
    pine_code_3 = """
    //@version=6
    indicator("RSI Strategy")
    rsi = ta.rsi(close, 14)
    if rsi > 70
        alert("Overbought")
    if rsi < 30
        alert("Oversold")
    plot(rsi)
    """
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: RSI with Conditions")
    print("=" * 60)
    print("\nPine Script Input:")
    print(pine_code_3)
    
    try:
        python_code = converter.convert(pine_code_3)
        print("\nGenerated Python Code:")
        print(python_code)
    except SyntaxError as e:
        print(f"Error: {e}")
