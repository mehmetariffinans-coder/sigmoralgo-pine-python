# Pine Script to Python Converter (AST Parser)

Professyonel Pine Script'i Python'a çeviren AST (Abstract Syntax Tree) temelli dönüştürücü.

## Mimari

```
Pine Script Input
    ↓
[Lexer] - Tokenization (Sözcüklere ayır)
    ↓
[Parser] - Build AST (Soyut sözdizim ağacı oluştur)
    ↓
[Semantic Analyzer] - Type checking, validation (Tür kontrol)
    ↓
[Code Generator] - Python code generation (Python kodu oluştur)
    ↓
Python Output (Backtrader/Pandas compatible)
```

## Özellikler

- ✅ Pine Script tokenization (Sözcükleme)
- ✅ AST generation (Soyut sözdizim ağacı)
- ✅ Pine to Python syntax conversion (Sözdizim dönüştürme)
- ✅ Indicators support (SMA, RSI, MACD, vb.)
- ✅ Strategy rules conversion (Strateji kuralları)
- ✅ Type checking and validation (Tür kontrolü)
- ✅ Error reporting with line numbers (Hata raporlama)

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```python
from converter import PineScriptConverter

converter = PineScriptConverter()
python_code = converter.convert_file('strategy.pine')
print(python_code)
```

## Proje Yapısı

```
├── pine_parser/
│   ├── __init__.py
│   ├── lexer.py              # Tokenization
│   ├── parser.py             # AST building
│   ├── ast_nodes.py          # AST node definitions
│   ├── token_types.py        # Token enumeration
│   ├── semantic_analyzer.py  # Type checking
│   └── code_generator.py     # Python code generation
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_converter.py
├── examples/
│   ├── simple_strategy.pine
│   └── advanced_strategy.pine
├── converter.py              # Main converter
├── requirements.txt
└── README.md
```

## Desteklenen Pine Script Özellikleri

### Temel
- Variables (var, int, float, bool, string)
- Functions ve method calls
- Operators (arithmetic, logical, comparison)
- Control flow (if/else, for, while)

### Built-in Functions
- close, open, high, low, volume
- time, bar_index, na

### Indicators (Technical Analysis)
- ta.sma (Simple Moving Average)
- ta.rsi (Relative Strength Index)
- ta.macd (MACD)
- ta.bb (Bollinger Bands)
- ta.atr (Average True Range)

### Strategy
- strategy.entry
- strategy.exit
- strategy.close
- strategy.order

## Örnek

### Pine Script Input
```pine
//@version=5
strategy("Simple Strategy", overlay=true)

fastLength = input(12, title="Fast Length")
slowLength = input(26, title="Slow Length")

fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

if fastMA > slowMA
    strategy.entry("Long", strategy.long)
else
    strategy.exit("Exit")
```

### Python Output
```python
import pandas as pd
import pandas_ta as ta
import backtrader as bt

class PineStrategy(bt.Strategy):
    params = (
        ('fast_length', 12),
        ('slow_length', 26),
    )
    
    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.params.fast_length
        )
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.params.slow_length
        )
    
    def next(self):
        if self.fast_ma[0] > self.slow_ma[0]:
            self.buy()
        else:
            self.close()
```

## Geliştirme

### Testleri çalıştır
```bash
pytest tests/ -v
```

### Code coverage
```bash
pytest tests/ --cov=pine_parser --cov-report=html
```

## Lisans

MIT
