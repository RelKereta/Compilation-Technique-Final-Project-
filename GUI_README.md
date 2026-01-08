# Chemical Reaction Compiler - GUI Documentation

## Overview
A beautiful, modern GUI built with Pygame that visualizes all 5 stages of the chemical reaction compiler in real-time.

**Version 2.0 Notes**: Now optimized for standard laptop screens with a compact 1000x700 resolution!

## Features

### 🎨 Modern Design
- **Dark Theme**: Professional dark mode interface with vibrant accent colors
- **Compact Layout**: Fits perfectly on smaller displays (1366x768 and up)
- **Smooth Animations**: Cursor blinking, hover effects, and smooth transitions
- **Scrollable Output**: All output areas support mouse wheel scrolling
- **Color-Coded Output**: Different colors for different types of information

### 🔧 Compilation Stages Visualization

#### Stage 1: Lexical Analysis
- Displays all tokens generated from input
- Shows token type and value
- Color-coded token list

#### Stage 2: Syntax Analysis
- Shows the parse tree structure
- Lists reactants and products
- Indicates if products need prediction

#### Stage 3: Semantic Analysis
- Shows prediction results
- Displays matched reaction rule
- Lists predicted products

#### Stage 4: Validation
- Shows validation status (✓ PASS or ✗ FAIL)
- Displays validation messages
- Checks atom conservation

#### Stage 5: Code Generation
- Generates multiple output formats:
  - **Python Code**: Executable Python representation
  - **Balanced Equation**: Chemical equation with coefficients
  - **Intermediate Representation (IR)**: Compiler IR code

## How to Use

### Running the GUI
```bash
python gui_compiler.py
```

### Using the Interface

1. **Enter a Reaction**
   - Click the input box at the top
   - Type a chemical reaction (e.g., `Na + Cl`, `HCl + NaOH`, `CH4 + O2`)
   - Press Enter or click "Compile"

2. **View Results**
   - Each stage displays its output in a separate panel
   - Scroll through output areas using the mouse wheel
   - Color-coded messages indicate success (green), errors (red), or warnings (yellow)

3. **Clear Output**
   - Click the "Clear" button to reset all outputs
   - Start fresh with a new reaction

### Example Reactions

#### Synthesis Reaction
```
Na + Cl
```
Predicts: NaCl (Sodium Chloride)

#### Neutralization Reaction
```
HCl + NaOH
```
Predicts: NaCl + H2O (Salt + Water)

#### Combustion Reaction
```
CH4 + O2
```
Predicts: CO2 + H2O (Carbon Dioxide + Water)

#### Complete Reaction (with products)
```
HCl + NaOH -> NaCl + H2O
```
Validates the provided products

#### Decomposition Reaction
```
KClO3
```
Predicts: KCl + O2

## UI Components

### Input Area
- **Input Box**: Type your chemical reaction here
- **Compile Button**: Process the reaction through all stages
- **Clear Button**: Reset all outputs

### Output Panels

| Panel | Description |
|-------|-------------|
| **Stage 1** | Lexical Analysis - Token list |
| **Stage 2** | Syntax Analysis - Parse tree |
| **Stage 3** | Semantic Analysis - Predictions |
| **Stage 4** | Validation - Validation results |
| **Stage 5** | Code Generation - Summary |
| **Output** | Complete generated code |

### Color Coding

- 🟢 **Green**: Success, valid results
- 🔴 **Red**: Errors, validation failures
- 🟡 **Yellow**: Warnings, predictions needed
- 🔵 **Blue**: Headers, section titles
- 🟣 **Purple**: Accent colors, highlights
- ⚪ **White**: Normal text
- ⚫ **Gray**: Dimmed text, metadata

## Keyboard Shortcuts

- **Enter**: Compile the current reaction
- **Backspace**: Delete characters in input
- **Mouse Wheel**: Scroll through output areas

## Technical Details

### Dependencies
- `pygame` - GUI framework
- `chem_lexer` - Lexical analyzer
- `chem_parser` - Syntax parser
- `chem_semantics` - Semantic analyzer
- `chem_codegen` - Code generator

### Window Specifications
- **Resolution**: 1000x700 pixels (Compact)
- **FPS**: 60 frames per second
- **Fonts**: Segoe UI (with fallbacks)

### Architecture
The GUI follows a component-based architecture:
- **Button**: Interactive buttons with hover effects
- **InputBox**: Text input with cursor animation
- **ScrollableTextArea**: Scrollable output display
- **CompilerGUI**: Main application controller

## Error Handling

The GUI gracefully handles:
- **Syntax Errors**: Invalid chemical formulas
- **Semantic Errors**: Invalid reaction combinations
- **Validation Errors**: Unbalanced equations
- **Empty Input**: Prevents compilation of empty strings

## Tips for Best Experience

1. **Try Different Reactions**: Experiment with various reaction types
2. **Scroll Through Output**: Use mouse wheel to see all generated code
3. **Read Validation Messages**: Understand why reactions pass or fail
4. **Compare Stages**: See how data transforms through each stage

## Troubleshooting

### GUI doesn't start
- Ensure Pygame is installed: `pip install pygame`
- Check Python version (3.7+ recommended)

### Text not displaying correctly
- The GUI uses fallback fonts if Segoe UI is unavailable
- All functionality remains intact with fallback fonts

### Scrolling not working
- Ensure mouse is over the output area
- Try scrolling slowly

## Future Enhancements

Potential improvements:
- Export generated code to file
- Reaction history
- Quick example buttons
- Syntax highlighting in code output
- Animation of compilation stages
- Dark/Light theme toggle

---

**Enjoy exploring the Chemical Reaction Compiler!** 🧪⚗️
