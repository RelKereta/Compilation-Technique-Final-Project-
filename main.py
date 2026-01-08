# main.py
import sys
from chem_lexer import Lexer
from chem_parser import Parser
from chem_semantics import Semantics
from chem_codegen import CodeGenerator

def main():
    print("=" * 60)
    print("Chemical Reaction Compiler (Full Pipeline)")
    print("=" * 60)
    print("Complete Compilation Stages:")
    print("1. Lexical Analysis → 2. Syntax Analysis → 3. Semantic Analysis")
    print("4. Validation → 5. Code Generation")
    print("\nType a reaction (e.g., 'HCl + NaOH') or 'exit' to quit.")
    print("Examples: Na + Cl | CH4 + O2 | HCl + NaOH -> NaCl + H2O")
    print("=" * 60)
    
    semantics = Semantics()
    codegen = CodeGenerator()

    while True:
        try:
            text = input("\n>>> Input: ")
            if text.lower() in ('exit', 'quit'):
                print("\nThank you for using the Chemical Reaction Compiler!")
                break
            
            if not text.strip():
                continue

            print("\n" + "-" * 60)
            
            # 1. Lexical Analysis
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            print(f"[STAGE 1: LEXER] Tokens: {tokens}")

            # 2. Syntax Analysis
            parser = Parser(tokens)
            reaction = parser.parse()
            print(f"[STAGE 2: PARSER] Parsed Structure: {reaction}")

            # 3. Semantic Analysis & Prediction
            # If products are missing, try to predict them
            if not reaction.products:
                print("[STAGE 3: SEMANTICS] Predicting products...")
                predicted_products, rule = semantics.predict_products(reaction.reactants)
                if predicted_products:
                    reaction.products = predicted_products
                    print(f"[STAGE 3: SEMANTICS] Matched Rule: {rule}")
                    print(f"[STAGE 3: SEMANTICS] Predicted Reaction: {reaction}")
                else:
                    print(f"[STAGE 3: SEMANTICS] No prediction rule matched.")
                    print(f"[STAGE 3: SEMANTICS] Reason: {rule}")
            else:
                print(f"[STAGE 3: SEMANTICS] Products provided: {' + '.join(str(p) for p in reaction.products)}")
            
            # 4. Validation
            is_valid, msg = semantics.validate_reaction(reaction)
            status = "✓ PASS" if is_valid else "✗ FAIL"
            print(f"[STAGE 4: VALIDATOR] {status} - {msg}")
            
            # 5. Code Generation (NEW!)
            if is_valid and reaction.products:
                print(f"\n[STAGE 5: CODE GENERATION] Generating executable code...")
                generated_code = codegen.generate(reaction)
                
                print(f"\n[RESULT] Final Balanced Reaction: {reaction}")
                print("\n" + "=" * 60)
                print("GENERATED CODE OUTPUTS:")
                print("=" * 60)
                
                # Show Python Code
                print("\n📄 Python Code:")
                print("-" * 60)
                print(generated_code['python'])
                
                # Show Balanced Equation
                print("\n⚖️  Balanced Equation:")
                print("-" * 60)
                print(generated_code['balanced'])
                
                # Show IR Code
                print("\n🔧 Intermediate Representation (IR):")
                print("-" * 60)
                print(generated_code['ir'])
                
                # Optionally show assembly (commented out by default)
                # print("\n⚙️  Assembly Code:")
                # print("-" * 60)
                # print(generated_code['assembly'])
                
                print("\n" + "=" * 60)
                print("✓ Compilation Complete!")
                print("=" * 60)
            
            print("-" * 60)

        except SyntaxError as e:
            print(f"\n[SYNTAX ERROR] {e}")
            print("Please check your input format.")
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
