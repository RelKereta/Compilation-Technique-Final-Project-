# GUI Quick Start Guide

## 🚀 Launch the GUI

```bash
python gui_compiler.py
```

## 📝 Quick Examples to Try

### 1. Simple Synthesis
**Input:** `Na + Cl`
- Watch the compiler predict NaCl
- See all 5 stages in action

### 2. Acid-Base Neutralization  
**Input:** `HCl + NaOH`
- Predicts salt (NaCl) and water (H2O)
- Shows balanced equation

### 3. Combustion
**Input:** `CH4 + O2`
- Predicts CO2 + H2O
- Demonstrates hydrocarbon combustion

### 4. With Products (Validation)
**Input:** `HCl + NaOH -> NaCl + H2O`
- Validates the provided products
- Checks atom conservation

### 5. Decomposition
**Input:** `KClO3`
- Single reactant decomposition
- Predicts KCl + O2

## 🎯 What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│  Chemical Reaction Compiler                                 │
│  Visualizing all 5 compilation stages                       │
├─────────────────────────────────────────────────────────────┤
│  [Input Box: Enter reaction]  [Compile] [Clear]            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Stage 1  │  │ Stage 2  │  │ Stage 3  │                 │
│  │  Lexer   │  │  Parser  │  │Semantics │                 │
│  │          │  │          │  │          │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌─────────────────────────┐                │
│  │ Stage 4  │  │      Stage 5            │                │
│  │Validator │  │   Code Generator        │                │
│  │          │  │                         │                │
│  └──────────┘  └─────────────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Generated Code Output                       │   │
│  │  • Python Code                                      │   │
│  │  • Balanced Equation                                │   │
│  │  • Intermediate Representation                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Color Guide

- **Green (✓)**: Success, validation passed
- **Red (✗)**: Error, validation failed  
- **Yellow**: Warnings, predictions
- **Blue**: Section headers
- **Purple**: Highlights and accents
- **White**: Normal output text
- **Gray**: Metadata and hints

## ⌨️ Controls

| Action | Method |
|--------|--------|
| Enter reaction | Click input box and type |
| Compile | Press Enter or click "Compile" |
| Clear all | Click "Clear" button |
| Scroll output | Mouse wheel over any panel |

## 💡 Pro Tips

1. **Start Simple**: Try `Na + Cl` first
2. **Watch All Stages**: Observe how data flows through each stage
3. **Read Predictions**: Stage 3 shows the chemical rule used
4. **Check Validation**: Stage 4 explains why reactions pass/fail
5. **Explore Code**: Scroll through the generated Python code

## 🐛 Common Issues

**Nothing happens when I click Compile?**
- Make sure you've typed something in the input box
- Check that the input box is active (has a blue border)

**Validation fails?**
- Read the validation message in Stage 4
- Some reactions may not be supported yet
- Try a simpler reaction first

**Can't see all the output?**
- Use mouse wheel to scroll in each panel
- Each panel scrolls independently

## 🎓 Learning Path

1. **Start**: Enter `Na + Cl`
2. **Observe**: Watch tokens appear in Stage 1
3. **Understand**: See how parser builds the structure in Stage 2
4. **Learn**: Read the prediction rule in Stage 3
5. **Verify**: Check validation in Stage 4
6. **Explore**: Scroll through generated code in Stage 5

---

**Have fun compiling chemical reactions!** 🧪✨
