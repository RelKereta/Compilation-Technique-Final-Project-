# test_chem_compiler.py
"""
Comprehensive unit tests for the Chemical Reaction Parser & Predictor
Tests lexer, parser, and semantic analysis components
"""

import unittest
from chem_lexer import Lexer, TOKEN_ELEMENT, TOKEN_NUMBER, TOKEN_PLUS, TOKEN_ARROW, TOKEN_EOF
from chem_parser import Parser, Molecule, Reaction
from chem_semantics import Semantics


class TestLexer(unittest.TestCase):
    """Test the lexical analysis component"""
    
    def test_simple_molecule(self):
        """Test tokenizing a simple molecule"""
        lexer = Lexer("H2O")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 4)  # H, 2, O, EOF
        self.assertEqual(tokens[0].type, TOKEN_ELEMENT)
        self.assertEqual(tokens[0].value, 'H')
        self.assertEqual(tokens[1].type, TOKEN_NUMBER)
        self.assertEqual(tokens[1].value, 2)
    
    def test_reaction_with_arrow(self):
        """Test tokenizing a reaction with arrow"""
        lexer = Lexer("H2 + O2 -> H2O")
        tokens = lexer.tokenize()
        arrow_tokens = [t for t in tokens if t.type == TOKEN_ARROW]
        self.assertEqual(len(arrow_tokens), 1)
        self.assertEqual(arrow_tokens[0].value, '->')
    
    def test_complex_formula(self):
        """Test tokenizing a complex formula with parentheses"""
        lexer = Lexer("Ca(OH)2")
        tokens = lexer.tokenize()
        # Ca, (, O, H, ), 2, EOF
        self.assertEqual(len(tokens), 7)
    
    def test_invalid_character(self):
        """Test that invalid characters raise errors"""
        lexer = Lexer("H2O@")
        with self.assertRaises(SyntaxError) as context:
            lexer.tokenize()
        self.assertIn("Invalid character", str(context.exception))


class TestParser(unittest.TestCase):
    """Test the syntax analysis component"""
    
    def test_parse_simple_molecule(self):
        """Test parsing a simple molecule"""
        lexer = Lexer("NaCl")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        self.assertEqual(len(reaction.reactants), 1)
        self.assertEqual(reaction.reactants[0].get_formula(), "NaCl")
    
    def test_parse_molecule_with_subscript(self):
        """Test parsing a molecule with subscripts"""
        lexer = Lexer("H2O")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        molecule = reaction.reactants[0]
        self.assertEqual(molecule.get_formula(), "H2O")
    
    def test_parse_reaction_with_products(self):
        """Test parsing a complete reaction"""
        lexer = Lexer("HCl + NaOH -> NaCl + H2O")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        self.assertEqual(len(reaction.reactants), 2)
        self.assertEqual(len(reaction.products), 2)
    
    def test_parse_multiple_reactants(self):
        """Test parsing multiple reactants"""
        lexer = Lexer("CH4 + O2")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        self.assertEqual(len(reaction.reactants), 2)
        self.assertEqual(len(reaction.products), 0)
    
    def test_parse_parentheses(self):
        """Test parsing molecules with parentheses"""
        lexer = Lexer("Ca(OH)2")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        molecule = reaction.reactants[0]
        # Should have Ca, O, H elements
        element_symbols = [e[0] for e in molecule.elements]
        self.assertIn('Ca', element_symbols)
        self.assertIn('O', element_symbols)
        self.assertIn('H', element_symbols)


class TestSemantics(unittest.TestCase):
    """Test the semantic analysis component"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.semantics = Semantics()
    
    def test_classify_hydrocarbon(self):
        """Test classification of hydrocarbons"""
        lexer = Lexer("CH4")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        molecule = reaction.reactants[0]
        classification = self.semantics.classify_compound(molecule)
        self.assertEqual(classification, "Hydrocarbon")
    
    def test_classify_acid(self):
        """Test classification of acids"""
        lexer = Lexer("HCl")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        molecule = reaction.reactants[0]
        classification = self.semantics.classify_compound(molecule)
        self.assertEqual(classification, "Acid")
    
    def test_classify_base(self):
        """Test classification of bases"""
        lexer = Lexer("NaOH")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        molecule = reaction.reactants[0]
        classification = self.semantics.classify_compound(molecule)
        self.assertEqual(classification, "Base")
    
    def test_synthesis_prediction(self):
        """Test synthesis reaction prediction"""
        lexer = Lexer("Na + Cl")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        products, rule = self.semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Synthesis")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].get_formula(), "NaCl")
    
    def test_synthesis_prediction_mg_o(self):
        """Test synthesis with different charges"""
        lexer = Lexer("Mg + O2")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        products, rule = self.semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Synthesis")
        self.assertEqual(products[0].get_formula(), "MgO")
    
    def test_acid_base_neutralization(self):
        """Test acid-base neutralization prediction"""
        lexer = Lexer("HCl + NaOH")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        products, rule = self.semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Acid-Base Neutralization")
        self.assertEqual(len(products), 2)  # Salt + Water
        # Check for water
        water_found = any(p.get_formula() == "H2O" for p in products)
        self.assertTrue(water_found)
    
    def test_combustion_prediction(self):
        """Test combustion reaction prediction"""
        lexer = Lexer("CH4 + O2")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        products, rule = self.semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Combustion")
        self.assertEqual(len(products), 2)  # CO2 + H2O
    
    def test_decomposition_prediction(self):
        """Test decomposition reaction prediction"""
        lexer = Lexer("KClO3")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        products, rule = self.semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Decomposition")
        self.assertEqual(len(products), 2)  # Compound + O2
    
    def test_invalid_metal_metal(self):
        """Test that metal-metal reactions are rejected"""
        lexer = Lexer("Na + K")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        is_valid, msg = self.semantics.validate_reaction(reaction)
        self.assertFalse(is_valid)
        self.assertIn("Metal-Metal", msg)
    
    def test_atom_conservation_valid(self):
        """Test atom conservation for a balanced reaction"""
        lexer = Lexer("H2 + O2 -> H2O")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        # This is intentionally unbalanced to test the validator
        is_valid, msg = self.semantics.validate_reaction(reaction)
        # Should fail because H2 + O2 != H2O (not balanced)
        self.assertFalse(is_valid)
        self.assertIn("not conserved", msg)
    
    def test_atom_conservation_balanced(self):
        """Test atom conservation for a properly balanced reaction"""
        # Manually create a balanced reaction: 2H2 + O2 -> 2H2O
        # Since we don't support coefficients, we'll test H2O2 -> H2 + O2
        lexer = Lexer("H2O2 -> H2 + O2")
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        is_valid, msg = self.semantics.validate_reaction(reaction)
        self.assertTrue(is_valid)
        self.assertIn("Valid", msg)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_complete_workflow_synthesis(self):
        """Test complete workflow: lexing -> parsing -> prediction -> validation"""
        text = "Na + Cl"
        
        # Lexical analysis
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        self.assertGreater(len(tokens), 0)
        
        # Syntax analysis
        parser = Parser(tokens)
        reaction = parser.parse()
        self.assertEqual(len(reaction.reactants), 2)
        
        # Semantic analysis
        semantics = Semantics()
        products, rule = semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Synthesis")
        
        # Update reaction with products
        reaction.products = products
        
        # Validation
        is_valid, msg = semantics.validate_reaction(reaction)
        self.assertTrue(is_valid)
    
    def test_complete_workflow_neutralization(self):
        """Test complete workflow for acid-base neutralization"""
        text = "HCl + NaOH"
        
        lexer = Lexer(text)
        parser = Parser(lexer.tokenize())
        reaction = parser.parse()
        
        semantics = Semantics()
        products, rule = semantics.predict_products(reaction.reactants)
        self.assertEqual(rule, "Acid-Base Neutralization")
        
        reaction.products = products
        is_valid, msg = semantics.validate_reaction(reaction)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
