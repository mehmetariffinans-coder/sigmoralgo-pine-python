# Pine Script 6 to Python Converter

## 📋 Przegląd

Profesjonalny konwerter Pine Script 6 (TradingView) na Python, oparty na architekturze AST (Abstract Syntax Tree).

### Obsługiwane wersje
- **Pine Script 6** ✅ (Full support)
- Pine Script 5 (Podstawowe wsparcie)

## 🏗️ Architektura

```
Pine Script Input
    ↓
[Lexer] - Tokenization (Leksykalna analiza)
    ↓
[Parser] - Build AST (Analiza składni)
    ↓
[Semantic Analyzer] - Type checking, validation (Analiza semantyczna)
    ↓
[Code Generator] - Python code generation (Generowanie kodu)
    ↓
Python Output (Backtrader/Pandas compatible)
```

## ✨ Cechy

### Podstawowe
- ✅ Pine Script 6 tokenization
- ✅ Pełna AST generation
- ✅ Pine to Python syntax conversion
- ✅ Type annotations support (Pine 6)
- ✅ Lambda expressions (Pine 6: `x => x * 2`)
- ✅ for...in loops (Pine 6)
- ✅ Power operator `**` (Pine 6)
- ✅ Arrays, Maps, Matrix types (Pine 6)
- ✅ Type checking and validation
- ✅ Error reporting with line/column numbers

### Funkcje Pine Script
- ✅ Technical Analysis (ta.sma, ta.ema, ta.rsi, ta.macd, etc.)
- ✅ Indicators support
- ✅ Strategy rules conversion
- ✅ Plot functions (plot, hline, fill, plotshape)
- ✅ String methods (Pine 6)
- ✅ Array methods (Pine 6)
- ✅ Request functions

## 📦 Instalacja

```bash
pip install -r requirements.txt
```

## 🚀 Użytkowanie

### Podstawowe użycie

```python
from converter import PineScriptConverter

converter = PineScriptConverter()
python_code, success = converter.convert("""
//@version=6
indicator("Moving Average", overlay=true)

fastMA = ta.sma(close, 12)
slowMA = ta.sma(close, 26)

plot(fastMA, color=color.blue)
plot(slowMA, color=color.red)
""")

if success:
    print(python_code)
else:
    print(converter.get_errors())
```

### Konwersja pliku

```python
converter = PineScriptConverter()
success = converter.convert_to_file('strategy.pine', 'strategy.py')

if success:
    print("Conversion successful!")
else:
    print(converter.get_errors())
```

## 📂 Struktura projektu

```
├── pine_parser/
│   ├── __init__.py              # Package initialization
│   ├── lexer.py                 # Tokenization (Pine 6)
│   ├── parser.py                # AST building (Pine 6)
│   ├── ast_nodes.py             # AST node definitions
│   ├── token_types.py           # Token enumeration
│   ├── semantic_analyzer.py     # Type checking (Pine 6)
│   └── code_generator.py        # Python code generation (Pine 6)
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_converter.py
├── examples/
│   ├── simple_indicator.pine
│   ├── moving_average_strategy.pine
│   └── advanced_strategy.pine
├── converter.py                 # Main converter
├── requirements.txt
└── README.md
```

## 🎯 Obsługiwane cechy Pine Script 6

### Kontrola przepływu
- ✅ `if/else` statements
- ✅ `for` loops (C-style)
- ✅ `for...in` loops (Pine 6)
- ✅ `while` loops
- ✅ `break` and `continue` (Pine 6)
- ✅ `return` statements

### Zmienne i typy
- ✅ `var` declarations
- ✅ Type annotations (Pine 6: `var x: int = 5`)
- ✅ Built-in types: int, float, bool, string
- ✅ Arrays (Pine 6: `array<type>`)
- ✅ Maps (Pine 6: `map<K,V>`)
- ✅ Matrix type (Pine 6)
- ✅ Custom types (Pine 6)

### Funkcje
- ✅ Function declarations
- ✅ Typed parameters (Pine 6)
- ✅ Return type annotations (Pine 6)
- ✅ Default parameter values (Pine 6)
- ✅ Lambda expressions (Pine 6: `x => x * 2`)
- ✅ @export decorator (Pine 6)

### Operatory
- ✅ Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (Pine 6)
- ✅ Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ Logical: `and`, `or`, `not`
- ✅ Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=` (Pine 6)
- ✅ Ternary: `a ? b : c`

### Dyrektywy Pine
- ✅ `@version=6`
- ✅ `indicator(...)`
- ✅ `strategy(...)`
- ✅ `library(...)` (Pine 6)
- ✅ `plot(...)`, `hline(...)`, `fill(...)`
- ✅ `plotshape(...)`, `plotchar(...)`

### Wbudowane funkcje

#### Technical Analysis (ta.*)
```
ta.sma, ta.ema, ta.rsi, ta.macd, ta.bb, ta.atr,
ta.stoch, ta.crossover, ta.crossunder
```

#### Matematyka
```
math.abs, math.sqrt, math.pow, math.log,
math.sin, math.cos, math.tan, math.min, math.max
```

#### Łańcuchy (Pine 6)
```
str.tostring, str.tonumber, str.contains,
str.replace, str.substring, str.upper, str.lower
```

#### Tablice (Pine 6)
```
array.new, array.push, array.pop, array.get,
array.set, array.size, array.clear, array.slice
```

#### Mapy (Pine 6)
```
map.new, map.put, map.get, map.remove, map.keys
```

#### Strategia
```
strategy.entry, strategy.exit, strategy.close,
strategy.order, strategy.cancel
```

## 📝 Przykłady

### Przykład 1: Prosty indykator

**Pine Script:**
```pine
//@version=6
indicator("Simple Moving Average", overlay=true)

fastLength = input(12, title="Fast Length")
slowLength = input(26, title="Slow Length")

fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

plot(fastMA, color=color.blue, title="Fast MA")
plot(slowMA, color=color.red, title="Slow MA")
```

**Python Output:**
```python
import numpy as np
import pandas as pd
import pandas_ta as ta
import backtrader as bt

fast_length = 12
slow_length = 26

fast_ma = ta.sma(close, fast_length)
slow_ma = ta.sma(close, slow_length)

plt.plot(fast_ma, label='Fast MA')
plt.plot(slow_ma, label='Slow MA')
```

### Przykład 2: Lambda expressions (Pine 6)

**Pine Script:**
```pine
//@version=6
indicator("Lambda Example")

arr = array.new<float>()
array.push(arr, 1.0)
array.push(arr, 2.0)
array.push(arr, 3.0)

// Lambda: x => x * 2
doubled = arr.map(x => x * 2)
```

**Python Output:**
```python
arr = []
arr.append(1.0)
arr.append(2.0)
arr.append(3.0)

# Lambda
doubled = list(map(lambda x: x * 2, arr))
```

### Przykład 3: for...in loops (Pine 6)

**Pine Script:**
```pine
//@version=6
indicator("For-In Example")

arr = array.new<int>()
array.push(arr, 10)
array.push(arr, 20)
array.push(arr, 30)

sum = 0
for value in arr
    sum += value
```

**Python Output:**
```python
arr = []
arr.append(10)
arr.append(20)
arr.append(30)

sum = 0
for value in arr:
    sum += value
```

## 🧪 Testowanie

```bash
# Uruchom wszystkie testy
pytest tests/ -v

# Code coverage
pytest tests/ --cov=pine_parser --cov-report=html

# Testuj konkretny moduł
pytest tests/test_lexer.py -v
```

## 📊 Porównanie Pine 5 vs Pine 6

| Cecha | Pine 5 | Pine 6 |
|-------|--------|--------|
| Type System | Luźny | Strict ✅ |
| Arrays | Nie | Tak ✅ |
| Maps | Nie | Tak ✅ |
| Lambda | Nie | Tak ✅ |
| for...in | Nie | Tak ✅ |
| Power operator `**` | Nie | Tak ✅ |
| Typed parameters | Nie | Tak ✅ |
| @export decorator | Nie | Tak ✅ |
| String methods | Nie | Tak ✅ |
| Matrix type | Nie | Tak ✅ |
| Custom types | Nie | Tak ✅ |

## 🐛 Znane ograniczenia

- Niektóre zaawansowane funkcje Backtrader mogą wymagać ręcznych dostosowań
- Series offset (`close[1]`) konwertowany na indeksowanie tablic
- Funkcje warunkowe wymagają jawnego cast do bool

## 📝 Licencja

MIT License - patrz LICENSE.md

## 👤 Autor

Mehmet Arif Finans - mehmetariffinans-coder

## 🤝 Wkład

Wkład jest mile widziany! Proszę otwórz Pull Request.
