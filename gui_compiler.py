# gui_compiler.py - Modern GUI for Chemical Reaction Compiler
"""
Beautiful Pygame GUI that visualizes all 5 compilation stages:
1. Lexical Analysis
2. Syntax Analysis  
3. Semantic Analysis
4. Validation
5. Code Generation
"""

import pygame
import sys
from chem_lexer import Lexer
from chem_parser import Parser
from chem_semantics import Semantics
from chem_codegen import CodeGenerator

# Initialize Pygame
pygame.init()

# Constants - RELEASE v2 (Compact Size)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# Modern Color Palette
COLORS = {
    'bg': (15, 18, 25),           # Dark background
    'surface': (25, 30, 40),      # Card background
    'surface_light': (35, 42, 55), # Lighter surface
    'primary': (99, 102, 241),    # Indigo
    'primary_hover': (129, 140, 248),
    'success': (34, 197, 94),     # Green
    'error': (239, 68, 68),       # Red
    'warning': (251, 191, 36),    # Amber
    'text': (248, 250, 252),      # Almost white
    'text_dim': (148, 163, 184),  # Gray
    'accent': (168, 85, 247),     # Purple
    'border': (51, 65, 85),       # Border gray
}

# Fonts
FONT_TITLE = None
FONT_HEADING = None
FONT_BODY = None
FONT_CODE = None

def init_fonts():
    """Initialize fonts with fallbacks"""
    global FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_CODE
    
    try:
        FONT_TITLE = pygame.font.SysFont('segoeui', 28, bold=True)
        FONT_HEADING = pygame.font.SysFont('segoeui', 18, bold=True)
        FONT_BODY = pygame.font.SysFont('segoeui', 14)
        FONT_CODE = pygame.font.SysFont('consolas', 12)
    except:
        FONT_TITLE = pygame.font.Font(None, 36)
        FONT_HEADING = pygame.font.Font(None, 22)
        FONT_BODY = pygame.font.Font(None, 18)
        FONT_CODE = pygame.font.Font(None, 16)

class Button:
    """Modern button with hover effects"""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        
        text_surf = FONT_BODY.render(self.text, True, COLORS['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class InputBox:
    """Modern input box with cursor"""
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif len(self.text) < 60:  # Max length
                self.text += event.unicode
        return False
        
    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
    def draw(self, screen):
        # Border color based on active state
        border_color = COLORS['primary'] if self.active else COLORS['border']
        
        # Draw background
        pygame.draw.rect(screen, COLORS['surface_light'], self.rect, border_radius=6)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=6)
        
        # Draw text or placeholder
        if self.text:
            text_surf = FONT_BODY.render(self.text, True, COLORS['text'])
        else:
            text_surf = FONT_BODY.render(self.placeholder, True, COLORS['text_dim'])
            
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)
        
        # Draw cursor
        if self.active and self.cursor_visible and self.text:
            cursor_x = text_rect.right + 2
            cursor_y = self.rect.y + 8
            pygame.draw.line(screen, COLORS['text'], 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + self.rect.height - 16), 2)

class ScrollableTextArea:
    """Scrollable text area for displaying output"""
    def __init__(self, x, y, width, height, title=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.lines = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def set_content(self, text, color=None):
        """Set content with optional color"""
        if color is None:
            color = COLORS['text']
        self.lines = []
        for line in text.split('\n'):
            self.lines.append((line, color))
        self.scroll_offset = 0
        
    def add_colored_lines(self, lines_with_colors):
        """Add lines with specific colors: [(text, color), ...]"""
        self.lines = lines_with_colors
        self.scroll_offset = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset -= event.y * 20
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                
    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, COLORS['surface'], self.rect, border_radius=6)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2, border_radius=6)
        
        # Draw title
        if self.title:
            title_surf = FONT_HEADING.render(self.title, True, COLORS['text'])
            screen.blit(title_surf, (self.rect.x + 10, self.rect.y + 10))
            content_y = self.rect.y + 40
        else:
            content_y = self.rect.y + 10
            
        # Create clipping rect for scrolling
        clip_rect = pygame.Rect(self.rect.x + 6, content_y, 
                               self.rect.width - 12, self.rect.height - (content_y - self.rect.y) - 6)
        screen.set_clip(clip_rect)
        
        # Draw lines
        y = content_y - self.scroll_offset
        line_height = 18
        
        for line_text, line_color in self.lines:
            if y > self.rect.y and y < self.rect.bottom:
                text_surf = FONT_CODE.render(line_text, True, line_color)
                screen.blit(text_surf, (self.rect.x + 10, y))
            y += line_height
            
        self.max_scroll = max(0, y - self.rect.bottom + 20)
        
        # Reset clip
        screen.set_clip(None)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = max(20, (self.rect.height / (y - content_y)) * self.rect.height)
            scrollbar_y = self.rect.y + (self.scroll_offset / self.max_scroll) * (self.rect.height - scrollbar_height)
            scrollbar_rect = pygame.Rect(self.rect.right - 6, scrollbar_y, 4, scrollbar_height)
            pygame.draw.rect(screen, COLORS['text_dim'], scrollbar_rect, border_radius=2)

class CompilerGUI:
    """Main GUI application"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chemical Reaction Compiler - Compact v2")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize fonts
        init_fonts()
        
        # Compiler components
        self.semantics = Semantics()
        self.codegen = CodeGenerator()
        
        # Layout Config
        MARGIN = 20
        INPUT_Y = 60
        ROW1_Y = 120
        ROW2_Y = 290
        ROW3_Y = 440
        
        ROW1_H = 160
        ROW2_H = 140
        ROW3_H = 240
        
        COL_W = 310
        LARGE_W = 640
        FULL_W = 960
        
        # UI Components
        self.input_box = InputBox(MARGIN, INPUT_Y, 450, 40, "Enter reaction (e.g., Na + Cl)")
        self.compile_button = Button(480, INPUT_Y, 100, 40, "Compile", COLORS['primary'], COLORS['primary_hover'])
        self.clear_button = Button(590, INPUT_Y, 80, 40, "Clear", COLORS['surface_light'], COLORS['border'])
        
        # Row 1: Stages 1, 2, 3
        self.stage1_area = ScrollableTextArea(MARGIN, ROW1_Y, COL_W, ROW1_H, "1. Lexer")
        self.stage2_area = ScrollableTextArea(MARGIN + COL_W + 15, ROW1_Y, COL_W, ROW1_H, "2. Parser")
        self.stage3_area = ScrollableTextArea(MARGIN + 2 * (COL_W + 15), ROW1_Y, COL_W, ROW1_H, "3. Semantics")
        
        # Row 2: Stages 4, 5
        self.stage4_area = ScrollableTextArea(MARGIN, ROW2_Y, COL_W, ROW2_H, "4. Validation")
        self.stage5_area = ScrollableTextArea(MARGIN + COL_W + 15, ROW2_Y, LARGE_W + 15, ROW2_H, "5. Code Generation")
        
        # Row 3: Output Code
        self.output_area = ScrollableTextArea(MARGIN, ROW3_Y, FULL_W, ROW3_H, "Generated Code Output")
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle input box
            if self.input_box.handle_event(event):
                self.compile_reaction()
                
            # Handle buttons
            if self.compile_button.handle_event(event):
                self.compile_reaction()
            if self.clear_button.handle_event(event):
                self.clear_all()
                
            # Handle scroll areas
            self.stage1_area.handle_event(event)
            self.stage2_area.handle_event(event)
            self.stage3_area.handle_event(event)
            self.stage4_area.handle_event(event)
            self.stage5_area.handle_event(event)
            self.output_area.handle_event(event)
            
    def update(self):
        """Update animations"""
        self.input_box.update()
        
    def draw(self):
        """Draw everything"""
        self.screen.fill(COLORS['bg'])
        
        # Draw title
        title_surf = FONT_TITLE.render("Chemical Reaction Compiler", True, COLORS['text'])
        self.screen.blit(title_surf, (20, 15))
        
        # Draw UI components
        self.input_box.draw(self.screen)
        self.compile_button.draw(self.screen)
        self.clear_button.draw(self.screen)
        
        # Draw output areas
        self.stage1_area.draw(self.screen)
        self.stage2_area.draw(self.screen)
        self.stage3_area.draw(self.screen)
        self.stage4_area.draw(self.screen)
        self.stage5_area.draw(self.screen)
        self.output_area.draw(self.screen)
        
        pygame.display.flip()
        
    def compile_reaction(self):
        """Compile the reaction and display results"""
        text = self.input_box.text.strip()
        if not text:
            return
            
        try:
            # Stage 1: Lexical Analysis
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            
            lines = []
            for i, token in enumerate(tokens):
                if token.type != 'EOF':
                    lines.append((f"{i+1}. {token}", COLORS['text']))
            self.stage1_area.add_colored_lines(lines)
            
            # Stage 2: Syntax Analysis
            parser = Parser(tokens)
            reaction = parser.parse()
            
            lines = [
                (f"R: {len(reaction.reactants)} mols", COLORS['success']),
            ]
            for r in reaction.reactants:
                lines.append((f" • {r}", COLORS['text']))
            
            lines.append((f"P: {len(reaction.products)} mols", 
                         COLORS['success'] if reaction.products else COLORS['warning']))
            if reaction.products:
                for p in reaction.products:
                    lines.append((f" • {p}", COLORS['text']))
            else:
                 lines.append((" (predicting...)", COLORS['text_dim']))
            self.stage2_area.add_colored_lines(lines)
            
            # Stage 3: Semantic Analysis
            lines = []
            if not reaction.products:
                predicted_products, rule = self.semantics.predict_products(reaction.reactants)
                if predicted_products:
                    reaction.products = predicted_products
                    lines.append(("✓ Prediction OK", COLORS['success']))
                    lines.append((f"Rule: {rule}", COLORS['text_dim']))
                    lines.append(("Result:", COLORS['text']))
                    for p in predicted_products:
                        lines.append((f" • {p}", COLORS['text']))
                else:
                    lines.append(("✗ Low Confidence", COLORS['error']))
                    lines.append((f"Reason: {rule}", COLORS['text_dim']))
            else:
                lines.append(("✓ Input Products OK", COLORS['success']))
                
            self.stage3_area.add_colored_lines(lines)
            
            # Stage 4: Validation
            is_valid, msg = self.semantics.validate_reaction(reaction)
            
            lines = []
            if is_valid:
                lines.append(("✓ PASS", COLORS['success']))
            else:
                lines.append(("✗ FAIL", COLORS['error']))
            lines.append((msg, COLORS['text']))
            
            self.stage4_area.add_colored_lines(lines)
            
            # Stage 5: Code Generation
            if is_valid and reaction.products:
                generated_code = self.codegen.generate(reaction)
                
                lines = [
                    ("Generation Complete!", COLORS['success']),
                    ("Outputs:", COLORS['text_dim']),
                    (" • Python Code", COLORS['text']),
                    (" • Balanced Eq", COLORS['text']),
                    (" • IR Code", COLORS['text']),
                ]
                self.stage5_area.add_colored_lines(lines)
                
                # Display generated code
                output_lines = [
                    ("--- PYTHON CODE ---", COLORS['primary']),
                ]
                
                for line in generated_code['python'].split('\n'):
                    output_lines.append((line, COLORS['text']))
                
                output_lines.extend([
                    ("", COLORS['text']),
                    ("--- BALANCED EQUATION ---", COLORS['primary']),
                ])
                
                for line in generated_code['balanced'].split('\n'):
                    output_lines.append((line, COLORS['success']))
                
                output_lines.extend([
                    ("", COLORS['text']),
                    ("--- INTERMEDIATE REPRESENTATION ---", COLORS['primary']),
                ])
                
                for line in generated_code['ir'].split('\n'):
                    output_lines.append((line, COLORS['text_dim']))
                
                self.output_area.add_colored_lines(output_lines)
            else:
                lines = [
                    ("Skipped", COLORS['warning']),
                    ("Fix validation errors first", COLORS['text_dim']),
                ]
                self.stage5_area.add_colored_lines(lines)
                self.output_area.set_content("No code generated.", COLORS['error'])
                
        except SyntaxError as e:
            error_msg = f"Syntax Error: {str(e)}"
            self.stage1_area.set_content(error_msg, COLORS['error'])
            self.stage2_area.set_content("Parsing failed", COLORS['error'])
            self.stage3_area.set_content("-", COLORS['text_dim'])
            self.stage4_area.set_content("-", COLORS['text_dim'])
            self.stage5_area.set_content("-", COLORS['text_dim'])
            self.output_area.set_content("Compilation failed.", COLORS['error'])
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.output_area.set_content(error_msg, COLORS['error'])
            
    def clear_all(self):
        """Clear all outputs"""
        self.input_box.text = ""
        self.stage1_area.set_content("")
        self.stage2_area.set_content("")
        self.stage3_area.set_content("")
        self.stage4_area.set_content("")
        self.stage5_area.set_content("")
        self.output_area.set_content("")

def main():
    """Main entry point"""
    app = CompilerGUI()
    app.run()

if __name__ == "__main__":
    main()
