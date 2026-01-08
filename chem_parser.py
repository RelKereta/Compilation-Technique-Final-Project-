# chem_parser.py
from chem_lexer import TOKEN_ELEMENT, TOKEN_NUMBER, TOKEN_PLUS, TOKEN_ARROW, TOKEN_EOF, TOKEN_LPAREN, TOKEN_RPAREN

class Molecule:
    def __init__(self, elements):
        self.elements = elements # List of (symbol, count) tuples

    def __repr__(self):
        res = ""
        for sym, count in self.elements:
            res += sym
            if count > 1:
                res += str(count)
        return res
    
    def get_formula(self):
        return self.__repr__()

class Reaction:
    def __init__(self, reactants, products=None):
        self.reactants = reactants
        self.products = products if products else []

    def __repr__(self):
        lhs = " + ".join([str(r) for r in self.reactants])
        rhs = " + ".join([str(p) for p in self.products])
        if self.products:
            return f"{lhs} -> {rhs}"
        return f"{lhs} -> ?"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        """Consume a token of the expected type, or raise an error"""
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"Unexpected token '{self.current_token.value}' (type: {self.current_token.type}). Expected {token_type}")

    def parse_molecule(self):
        """
        Parse a molecule according to the grammar:
        Molecule → ElementGroup+
        ElementGroup → Element Number? | '(' Element+ ')' Number?
        
        Examples: H2O, Ca(OH)2, NaCl, O2
        """
        # Molecule -> (Element Number?)+
        # Simplified: We just grab a sequence of Elements and Numbers
        elements = []
        
        # Check if we have a valid start of a molecule
        if self.current_token.type not in (TOKEN_ELEMENT, TOKEN_LPAREN):
             raise SyntaxError(f"Expected Element or '(', got {self.current_token}")

        while self.current_token.type in (TOKEN_ELEMENT, TOKEN_LPAREN):
            if self.current_token.type == TOKEN_ELEMENT:
                sym = self.current_token.value
                self.eat(TOKEN_ELEMENT)
                count = 1
                if self.current_token.type == TOKEN_NUMBER:
                    count = self.current_token.value
                    self.eat(TOKEN_NUMBER)
                elements.append((sym, count))
            elif self.current_token.type == TOKEN_LPAREN:
                # Handle groups like (OH)2
                self.eat(TOKEN_LPAREN)
                group_elements = []
                while self.current_token.type == TOKEN_ELEMENT:
                    sym = self.current_token.value
                    self.eat(TOKEN_ELEMENT)
                    count = 1
                    if self.current_token.type == TOKEN_NUMBER:
                        count = self.current_token.value
                        self.eat(TOKEN_NUMBER)
                    group_elements.append((sym, count))
                self.eat(TOKEN_RPAREN)
                
                group_count = 1
                if self.current_token.type == TOKEN_NUMBER:
                    group_count = self.current_token.value
                    self.eat(TOKEN_NUMBER)
                
                # Flatten group
                for sym, count in group_elements:
                    elements.append((sym, count * group_count))

        return Molecule(elements)

    def parse_reaction(self):
        """
        Parse a chemical reaction according to the grammar:
        Reaction → Reactants (→ Products)?
        Reactants → Molecule (+ Molecule)*
        Products → Molecule (+ Molecule)*
        
        Examples: 
        - HCl + NaOH -> NaCl + H2O
        - CH4 + O2
        - KClO3 -> KCl + O2
        """
        # Reaction -> Reactants (-> Products)?
        reactants = []
        reactants.append(self.parse_molecule())
        
        while self.current_token.type == TOKEN_PLUS:
            self.eat(TOKEN_PLUS)
            reactants.append(self.parse_molecule())
            
        products = []
        if self.current_token.type == TOKEN_ARROW:
            self.eat(TOKEN_ARROW)
            # If we have an arrow, we expect products, unless it's just a query
            if self.current_token.type != TOKEN_EOF:
                products.append(self.parse_molecule())
                while self.current_token.type == TOKEN_PLUS:
                    self.eat(TOKEN_PLUS)
                    products.append(self.parse_molecule())
        
        if self.current_token.type != TOKEN_EOF:
             raise SyntaxError(f"Unexpected token at end: {self.current_token}. Expected end of input.")

        return Reaction(reactants, products)

    def parse(self):
        return self.parse_reaction()
