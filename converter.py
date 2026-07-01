"""Main converter module - orchestrates Pine Script 6 to Python conversion"""

from typing import Tuple, List
from pine_parser.lexer import Lexer
from pine_parser.parser import Parser
from pine_parser.semantic_analyzer import SemanticAnalyzer
from pine_parser.code_generator import CodeGenerator


class PineScriptConverter:
    """Converts Pine Script 6 code to Python"""
    
    def __init__(self):
        self.last_errors: List[str] = []
        self.last_warnings: List[str] = []
    
    def convert(self, code: str) -> Tuple[str, bool]:
        """
        Convert Pine Script 6 code to Python.
        
        Args:
            code: Pine Script 6 source code
        
        Returns:
            Tuple of (generated_python_code, success_boolean)
        """
        try:
            # Step 1: Lexical analysis
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Step 2: Syntax analysis
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Step 3: Semantic analysis
            analyzer = SemanticAnalyzer()
            success = analyzer.analyze(ast)
            
            self.last_errors = analyzer.get_errors()
            self.last_warnings = analyzer.get_warnings()
            
            if not success:
                return "", False
            
            # Step 4: Code generation
            generator = CodeGenerator()
            python_code = generator.generate(ast)
            
            return python_code, True
        
        except SyntaxError as e:
            self.last_errors = [str(e)]
            return "", False
        except Exception as e:
            self.last_errors = [f"Unexpected error: {str(e)}"]
            return "", False
    
    def convert_file(self, filepath: str) -> Tuple[str, bool]:
        """
        Convert Pine Script 6 file to Python.
        
        Args:
            filepath: Path to Pine Script file
        
        Returns:
            Tuple of (generated_python_code, success_boolean)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.convert(code)
        except FileNotFoundError:
            self.last_errors = [f"File not found: {filepath}"]
            return "", False
        except Exception as e:
            self.last_errors = [f"Error reading file: {str(e)}"]
            return "", False
    
    def convert_to_file(self, input_path: str, output_path: str) -> bool:
        """
        Convert Pine Script file and write to output file.
        
        Args:
            input_path: Input Pine Script file path
            output_path: Output Python file path
        
        Returns:
            Success boolean
        """
        python_code, success = self.convert_file(input_path)
        
        if not success:
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
            return True
        except Exception as e:
            self.last_errors = [f"Error writing file: {str(e)}"]
            return False
    
    def get_errors(self) -> List[str]:
        """Get last conversion errors"""
        return self.last_errors
    
    def get_warnings(self) -> List[str]:
        """Get last conversion warnings"""
        return self.last_warnings
