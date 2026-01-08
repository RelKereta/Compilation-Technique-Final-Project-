# chem_lexer.py
import re

# Token Types
TOKEN_ELEMENT = 'ELEMENT'
TOKEN_NUMBER = 'NUMBER'
TOKEN_PLUS = 'PLUS'
TOKEN_ARROW = 'ARROW'
TOKEN_EOF = 'EOF'
TOKEN_LPAREN = 'LPAREN' # Optional, for complex formulas like Ca(OH)2
TOKEN_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = self.input_text[self.pos] if self.input_text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def element(self):
        # Elements start with Uppercase, optionally followed by Lowercase
        result = ''
        if self.current_char is not None and self.current_char.isupper():
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.islower():
                result += self.current_char
                self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TOKEN_NUMBER, self.number())

            if self.current_char.isupper():
                return Token(TOKEN_ELEMENT, self.element())

            if self.current_char == '+':
                self.advance()
                return Token(TOKEN_PLUS, '+')

            if self.current_char == '-':
                # Check for arrow '->'
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token(TOKEN_ARROW, '->')
                else:
                    raise SyntaxError(f"Unexpected character '{self.current_char}' at position {self.pos}. Expected '>' after '-'")
            
            # Handle unicode arrow if user pastes it
            if self.current_char == '→':
                self.advance()
                return Token(TOKEN_ARROW, '->')

            if self.current_char == '(':
                self.advance()
                return Token(TOKEN_LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TOKEN_RPAREN, ')')

            raise SyntaxError(f"Invalid character '{self.current_char}' at position {self.pos}")

        return Token(TOKEN_EOF, None)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TOKEN_EOF:
                break
        return tokens

# Simple test if run directly
if __name__ == '__main__':
    text = "NaOH + HCl -> NaCl + H2O"
    lexer = Lexer(text)
    print(lexer.tokenize())
