# Chemical Reaction Compiler

A complete compiler implementation that parses and analyzes chemical reactions using compilation techniques.

## 🎯 Project Overview

This project demonstrates a **full 5-stage compiler** applied to chemical reactions:

1. **Lexical Analysis** - Tokenization of chemical formulas
2. **Syntax Analysis** - Recursive Descent Parsing with LL(1) grammar
3. **Semantic Analysis** - Compound classification and product prediction
4. **Validation** - Atom conservation and error checking
5. **Code Generation** - Executable Python code generation

## 📁 Project Structure

```
Compilation-Technique-Final-Project--main/
├── chem_lexer.py          # Stage 1: Lexical Analyzer
├── chem_parser.py         # Stage 2: Syntax Analyzer (Parser)
├── chem_semantics.py      # Stage 3 & 4: Semantic Analyzer + Validator
├── chem_codegen.py        # Stage 5: Code Generator
├── chem_utils.py          # Utility functions for chemistry
├── main.py                # Main compiler driver (CLI)
├── demo_compiler.py       # Demonstration script
├── test_chem_compiler.py  # Test suite
├── README.md              # This file
├── COMPILER_SUMMARY.md    # Detailed compiler explanation
├── CORRECT_PARSE_TREES.md # Parse tree documentation
└── REQUIREMENTS_COMPLIANCE.md # Requirements checklist
```

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
```

### Installation
```bash
# No external dependencies required!
# All modules use Python standard library
```

### Running the Compiler

**Interactive Mode:**
```bash
python main.py
```

**Example Session:**
```
>>> Input: HCl + NaOH

[STAGE 1: LEXER] Tokens: [ELEMENT(H), ELEMENT(Cl), PLUS, ...]
[STAGE 2: PARSER] Parsed Structure: HCl + NaOH
[STAGE 3: SEMANTICS] Predicted Products: NaCl + H2O
[STAGE 4: VALIDATOR] ✓ PASS - Atoms conserved
[STAGE 5: CODE GENERATION] Generating executable code...

📄 Generated Python Code:
class Molecule:
    def __init__(self, formula, elements):
        self.formula = formula
        self.elements = elements

reactant_1 = Molecule('HCl', {'H': 1, 'Cl': 1})
...

✓ Compilation Complete!
```

**Demo Mode:**
```bash
python demo_compiler.py
```

**Run Tests:**
```bash
python test_chem_compiler.py
```

## 📖 Grammar Specification

### EBNF Grammar
```
<reaction>      ::= <reactants> ("->" <products>)? EOF
<reactants>     ::= <molecule> ("+" <molecule>)*
<products>      ::= <molecule> ("+" <molecule>)*
<molecule>      ::= <element_group>+
<element_group> ::= ELEMENT NUMBER?
                  | "(" ELEMENT+ ")" NUMBER?
```

### Grammar Properties
- **Type:** LL(1) - suitable for top-down parsing
- **Parsing Method:** Recursive Descent Parsing (RDP)
- **Complexity:** O(n) where n is input length
- **Ambiguity:** Unambiguous

### Terminal Symbols
- `ELEMENT` - Chemical element symbol (e.g., H, O, Na, Cl)
- `NUMBER` - Subscript number (e.g., 2, 3, 10)
- `PLUS` - Addition operator (+)
- `ARROW` - Reaction arrow (->)
- `LPAREN` - Left parenthesis (()
- `RPAREN` - Right parenthesis ())
- `EOF` - End of input

## 🔬 Supported Reaction Types

### 1. Synthesis
```
Input:  Na + Cl
Output: Na + Cl -> NaCl
```

### 2. Combustion
```
Input:  CH4 + O2
Output: CH4 + O2 -> CO2 + H2O
```

### 3. Neutralization
```
Input:  HCl + NaOH
Output: HCl + NaOH -> NaCl + H2O
```

### 4. Decomposition
```
Input:  KClO3
Output: KClO3 -> KCl + O2
```

## 🎓 Compilation Stages Explained

### Stage 1: Lexical Analysis (`chem_lexer.py`)
**Input:** Raw text string
**Output:** Token stream
**Example:**
```
Input:  "H2O"
Output: [ELEMENT(H), NUMBER(2), ELEMENT(O), EOF]
```

### Stage 2: Syntax Analysis (`chem_parser.py`)
**Input:** Token stream
**Output:** Abstract Syntax Tree (AST)
**Method:** Recursive Descent Parsing
**Example:**
```
Parse Tree:
reaction
├── reactants
│   └── molecule: H2O
│       ├── element_group: H (×2)
│       └── element_group: O
└── EOF
```

### Stage 3: Semantic Analysis (`chem_semantics.py`)
**Input:** AST
**Output:** Validated and enriched AST
**Functions:**
- Compound classification (Metal, Acid, Base, etc.)
- Product prediction using semantic rules
- Type checking

**Example:**
```
Input:  Na + Cl
Classification: Metal + Non-metal
Prediction: Synthesis → NaCl
```

### Stage 4: Validation (`chem_semantics.py`)
**Input:** Enriched AST
**Output:** Validation result
**Checks:**
- Atom conservation (mass balance)
- Invalid reactant combinations
- Structural validity

### Stage 5: Code Generation (`chem_codegen.py`)
**Input:** Validated AST
**Output:** Executable code
**Formats:**
1. Python code (executable)
2. Balanced equation
3. Intermediate Representation (IR)
4. Stoichiometry calculator
5. Assembly-like code (educational)

## 💡 Key Features

### Compiler Techniques Used
- ✅ **Tokenization** - Pattern matching for lexical analysis
- ✅ **Recursive Descent Parsing** - Top-down syntax analysis
- ✅ **LL(1) Grammar** - Efficient predictive parsing
- ✅ **Type Checking** - Compound classification
- ✅ **Semantic Rules** - Reaction type prediction
- ✅ **Symbol Table** - Compound type storage
- ✅ **Error Recovery** - Graceful error handling
- ✅ **Code Generation** - Multiple output formats

### Novel Application
This project applies **compiler techniques to chemistry**:
- Uses semantic analysis for product prediction
- Applies type checking to chemical compounds
- Generates executable code from chemical reactions
- Demonstrates that compiler concepts extend beyond programming languages

## 📊 Example Outputs

### Complete Compilation Example

**Input:** `HCl + NaOH`

**Stage 1 - Tokens:**
```
[ELEMENT(H), ELEMENT(Cl), PLUS, ELEMENT(Na), ELEMENT(O), ELEMENT(H), EOF]
```

**Stage 2 - Parse Tree:**
```
Reaction
├── Reactants
│   ├── Molecule: HCl
│   └── Molecule: NaOH
└── Products: (to be predicted)
```

**Stage 3 - Semantic Analysis:**
```
Reactant Types: [Acid, Ionic Compound]
Predicted Type: ⚖️ Neutralization
Predicted Products: NaCl + H2O
```

**Stage 4 - Validation:**
```
✓ PASS - Atoms conserved
Reactants: H(2), Cl(1), Na(1), O(1)
Products:  H(2), Cl(1), Na(1), O(1)
```

**Stage 5 - Generated Code:**
```python
# Generated Python Code
class Molecule:
    def __init__(self, formula, elements):
        self.formula = formula
        self.elements = elements

reactant_1 = Molecule('HCl', {'H': 1, 'Cl': 1})
reactant_2 = Molecule('NaOH', {'Na': 1, 'O': 1, 'H': 1})
product_1 = Molecule('NaCl', {'Na': 1, 'Cl': 1})
product_2 = Molecule('H2O', {'H': 2, 'O': 1})

print("Reaction: HCl + NaOH -> NaCl + H2O")
```

## 🧪 Testing

Run the test suite:
```bash
python test_chem_compiler.py
```

Tests include:
- Lexical analysis tests
- Parser tests
- Semantic analysis tests
- Validation tests
- Code generation tests
- Integration tests

## 📚 Documentation

- **README.md** (this file) - Project overview and usage
- **COMPILER_SUMMARY.md** - Detailed explanation of all 5 stages
- **CORRECT_PARSE_TREES.md** - Parse tree examples and grammar
- **REQUIREMENTS_COMPLIANCE.md** - Requirements checklist

## 🎯 Project Goals

This project demonstrates:
1. Complete understanding of compilation stages
2. Implementation of a working compiler
3. Novel application of compiler techniques
4. Professional code quality and documentation

## 📝 License

Educational project for Compilation Techniques course.

## 👨‍💻 Author

Created as a final project for COMP6062001 - Compilation Techniques

---

**Note:** This is a simplified, educational compiler. For production use, consider:
- More sophisticated balancing algorithms
- Additional reaction types
- Quantum chemistry calculations
- Database of known reactions
