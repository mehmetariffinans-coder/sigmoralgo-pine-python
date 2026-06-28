"""Main Pine Script to Python Converter"""

from pine_parser import Lexer, Parser, CodeGenerator, SemanticAnalyzer

class PineScriptConverter:
    """Main converter class for Pine Script to Python"""
    
    def __init__(self):
        self.errors = []
    
    def convert(self, pine_code: str) -> str:
        """Convert Pine Script code to Python
        
        Args:
            pine_code: Pine Script source code
        
        Returns:
            Python source code
        
        Raises:
            SyntaxError: If there are syntax errors in the input
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
    # Example usage
    pine_code = """
    var x = close > open
    if x
        var y = 5
    """
    
    converter = PineScriptConverter()
    try:
        python_code = converter.convert(pine_code)
        print("Generated Python Code:")
        print(python_code)
    except SyntaxError as e:
        print(f"Error: {e}")
