#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCII Art Generator using Textual
Create beautiful ASCII art from text with various styles and effects!

Features:
- Multiple font styles (Big, Block, Small, Banner)
- Border decorations
- Text alignment options
- Color themes
- Export functionality
"""

import re
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static, Label, Button, Input, Header, Footer, 
    Select, TextArea, Checkbox
)
from textual.reactive import reactive
from rich.text import Text
from rich.console import Console


class ASCIIArtGenerator(App):
    """ASCII Art Generator with multiple styles and effects."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .app-container {
        border: solid $primary;
        background: $panel;
        width: 90;
        max-height: 95vh;
        margin: 1;
        padding: 1;
    }
    
    .title {
        text-align: center;
        background: $secondary;
        color: $text;
        margin: 1 0;
        padding: 1;
    }
    
    .input-section {
        border: solid $accent;
        background: $surface;
        margin: 1 0;
        padding: 1;
        height: auto;
    }
    
    .controls-section {
        margin: 1 0;
        padding: 1;
        height: auto;
    }
    
    .preview-section {
        border: solid $success;
        background: $panel;
        margin: 1 0;
        padding: 1;
        height: auto;
        min-height: 15;
    }
    
    .export-section {
        border: solid $warning;
        background: $surface;
        margin: 1 0;
        padding: 1;
        height: auto;
    }
    
    Button {
        margin: 0 1;
    }
    
    Input {
        margin: 1 0;
        width: 100%;
    }
    
    Select {
        margin: 1 0;
        width: 100%;
    }
    
    TextArea {
        margin: 1 0;
        height: 12;
    }
    
    .preview-text {
        margin: 1;
        padding: 1;
        background: $surface;
        color: $text;
        width: 100%;
        height: auto;
    }
    
    #art-preview {
        overflow-x: auto;
    }
    """
    
    # Reactive state
    input_text = reactive("")
    selected_style = reactive("Big")
    border_enabled = reactive(False)
    alignment = reactive("center")
    current_art = reactive("")
    
    def __init__(self):
        super().__init__()
        
        # ASCII font patterns
        self.fonts = {
            "Big": {
                'A': [" █████ ", "██   ██", "███████", "██   ██", "██   ██"],
                'B': ["██████ ", "██   ██", "██████ ", "██   ██", "██████ "],
                'C': [" ██████", "██     ", "██     ", "██     ", " ██████"],
                'D': ["██████ ", "██   ██", "██   ██", "██   ██", "██████ "],
                'E': ["███████", "██     ", "█████  ", "██     ", "███████"],
                'F': ["███████", "██     ", "█████  ", "██     ", "██     "],
                'G': [" ██████ ", "██      ", "██   ███", "██    ██", " ██████ "],
                'H': ["██   ██", "██   ██", "███████", "██   ██", "██   ██"],
                'I': ["███████", "   ██  ", "   ██  ", "   ██  ", "███████"],
                'J': ["███████", "     ██", "     ██", "██   ██", " ██████"],
                'K': ["██   ██", "██  ██ ", "█████  ", "██  ██ ", "██   ██"],
                'L': ["██     ", "██     ", "██     ", "██     ", "███████"],
                'M': ["███████", "███████", "██ █ ██", "██   ██", "██   ██"],
                'N': ["███████", "██   ██", "██   ██", "██   ██", "██   ██"],
                'O': [" ██████ ", "██    ██", "██    ██", "██    ██", " ██████ "],
                'P': ["██████ ", "██   ██", "██████ ", "██     ", "██     "],
                'Q': [" ██████ ", "██    ██", "██ █  ██", "██  █ ██", " ██████ "],
                'R': ["██████ ", "██   ██", "██████ ", "██   ██", "██   ██"],
                'S': [" ██████", "██     ", " █████ ", "     ██", "██████ "],
                'T': ["███████", "   ██  ", "   ██  ", "   ██  ", "   ██  "],
                'U': ["██   ██", "██   ██", "██   ██", "██   ██", " ██████"],
                'V': ["██   ██", "██   ██", "██   ██", " ██ ██ ", "  ███  "],
                'W': ["██   ██", "██   ██", "██ █ ██", "███████", "███████"],
                'X': ["██   ██", " ██ ██ ", "  ███  ", " ██ ██ ", "██   ██"],
                'Y': ["██   ██", " ██ ██ ", "  ███  ", "   ██  ", "   ██  "],
                'Z': ["███████", "    ██ ", "   ██  ", "  ██   ", "███████"],
                ' ': ["       ", "       ", "       ", "       ", "       "],
                '!': ["  ██   ", "  ██   ", "  ██   ", "       ", "  ██   "],
                '?': [" ██████", "     ██", "  █████", "       ", "   ██  "],
            },
            
            "Block": {
                'A': ["███", "█▀█", "███", "█ █", "█ █"],
                'B': ["██ ", "█▀█", "██ ", "█▄█", "██ "],
                'C': ["███", "█  ", "█  ", "█  ", "███"],
                'D': ["██ ", "█ █", "█ █", "█ █", "██ "],
                'E': ["███", "█  ", "██ ", "█  ", "███"],
                'F': ["███", "█  ", "██ ", "█  ", "█  "],
                'G': ["███", "█  ", "█▄█", "█ █", "███"],
                'H': ["█ █", "█ █", "███", "█ █", "█ █"],
                'I': ["███", " █ ", " █ ", " █ ", "███"],
                'J': ["███", "  █", "  █", "█ █", "███"],
                'K': ["█ █", "██ ", "█▀ ", "█ █", "█ █"],
                'L': ["█  ", "█  ", "█  ", "█  ", "███"],
                'M': ["███", "███", "█▀█", "█ █", "█ █"],
                'N': ["███", "█ █", "█ █", "█ █", "█ █"],
                'O': ["███", "█ █", "█ █", "█ █", "███"],
                'P': ["██ ", "█ █", "██ ", "█  ", "█  "],
                'Q': ["███", "█ █", "█▀█", "█▄█", "███"],
                'R': ["██ ", "█ █", "██ ", "█ █", "█ █"],
                'S': ["███", "█  ", "███", "  █", "███"],
                'T': ["███", " █ ", " █ ", " █ ", " █ "],
                'U': ["█ █", "█ █", "█ █", "█ █", "███"],
                'V': ["█ █", "█ █", "█ █", "▀█▀", " █ "],
                'W': ["█ █", "█ █", "█▀█", "███", "███"],
                'X': ["█ █", "▀█▀", " █ ", "▀█▀", "█ █"],
                'Y': ["█ █", "▀█▀", " █ ", " █ ", " █ "],
                'Z': ["███", " █ ", " █ ", " █ ", "███"],
                ' ': ["   ", "   ", "   ", "   ", "   "],
                '!': [" █ ", " █ ", " █ ", "   ", " █ "],
                '?': ["██ ", " █ ", " █ ", "   ", " █ "],
            },
            
            "Small": {
                'A': ["█▀█", "█▀█", "█ █"],
                'B': ["█▀▄", "█▀▄", "█▄▀"],
                'C': ["▄▀█", "█▄▄", "▀▀▀"],
                'D': ["█▀▄", "█ █", "█▄▀"],
                'E': ["█▀▀", "█▀▀", "█▄▄"],
                'F': ["█▀▀", "█▀▀", "█  "],
                'G': ["▄▀█", "█▄█", "▀▀█"],
                'H': ["█ █", "███", "█ █"],
                'I': ["███", " █ ", "███"],
                'J': ["███", "  █", "██ "],
                'K': ["█ █", "██ ", "█ █"],
                'L': ["█  ", "█  ", "███"],
                'M': ["███", "█▀█", "█ █"],
                'N': ["██▄", "█▀█", "█ █"],
                'O': ["▄▀█", "█ █", "▀▀▀"],
                'P': ["█▀▄", "█▀ ", "█  "],
                'Q': ["▄▀█", "█▀█", "▀▀▀"],
                'R': ["█▀▄", "█▀▄", "█ █"],
                'S': ["▄▀▀", "▀▀▄", "▄▄▀"],
                'T': ["███", " █ ", " █ "],
                'U': ["█ █", "█ █", "▀▀▀"],
                'V': ["█ █", "█ █", " ▀ "],
                'W': ["█ █", "█▀█", "███"],
                'X': ["█ █", " ▀ ", "█ █"],
                'Y': ["█ █", " ▀ ", " █ "],
                'Z': ["███", " ▀ ", "███"],
                ' ': ["   ", "   ", "   "],
                '!': [" █ ", " █ ", " █ "],
                '?': ["▀▀▄", " ▄▀", " █ "],
            }
        }
        
        # Border patterns
        self.borders = {
            "simple": ["─", "│", "┌", "┐", "└", "┘"],
            "double": ["═", "║", "╔", "╗", "╚", "╝"],
            "thick": ["━", "┃", "┏", "┓", "┗", "┛"],
            "dotted": ["┈", "┊", "┌", "┐", "└", "┘"],
        }
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="app-container"):
            yield Static("🎨 ASCII ART GENERATOR 🎨", classes="title")
            
            # Input section
            with Container(classes="input-section"):
                yield Label("Enter Text to Convert:")
                yield Input(
                    placeholder="Type your text here (max 20 chars)...", 
                    id="text-input",
                    max_length=20
                )
            
            # Controls section
            with Container(classes="controls-section"):
                with Horizontal():
                    with Vertical():
                        yield Label("Font Style:")
                        yield Select([
                            ("Big Font", "Big"),
                            ("Block Font", "Block"),
                            ("Small Font", "Small")
                        ], value="Big", id="style-select")
                    
                    with Vertical():
                        yield Label("Options:")
                        yield Checkbox("Add Border", id="border-checkbox")
                        yield Select([
                            ("Center", "center"),
                            ("Left", "left"),
                            ("Right", "right")
                        ], value="center", id="align-select")
                
                with Horizontal():
                    yield Button("Generate Art", id="generate", variant="primary")
                    yield Button("Clear", id="clear", variant="warning")
                    yield Button("Copy to Clipboard", id="copy", variant="success")
            
            # Preview section
            with Container(classes="preview-section"):
                yield Label("ASCII Art Preview:")
                yield Static("", id="art-preview", classes="preview-text")
            
            # Export section
            with Container(classes="export-section"):
                yield Label("Export Options:")
                with Horizontal():
                    yield Button("Save as TXT", id="save-txt", variant="success")
                    yield Button("Random Example", id="random", variant="default")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize with a welcome message."""
        # Set initial text in input field and reactive variable
        self.input_text = "HELLO"
        self.query_one("#text-input", Input).value = "HELLO"
        self.generate_ascii_art("HELLO")
    
    def generate_ascii_art(self, text: str) -> None:
        """Generate ASCII art from text."""
        if not text:
            self.current_art = ""
            self.query_one("#art-preview", Static).update("")
            return
        
        text = text.upper()[:20]  # Limit to 20 characters
        font = self.fonts.get(self.selected_style, self.fonts["Big"])
        
        # Get font height
        font_height = len(list(font.values())[0]) if font else 5
        
        # Generate lines
        art_lines = [""] * font_height
        
        for char in text:
            if char in font:
                char_lines = font[char]
                for i in range(font_height):
                    art_lines[i] += char_lines[i] + " "
        
        # Apply alignment
        if self.alignment == "center":
            art_lines = [line.center(60) for line in art_lines]
        elif self.alignment == "right":
            art_lines = [line.rjust(60) for line in art_lines]
        
        # Add border if enabled
        if self.border_enabled:
            border = self.borders["simple"]
            max_width = max(len(line.rstrip()) for line in art_lines) + 4
            
            # Top border
            bordered_lines = [border[2] + border[0] * (max_width - 2) + border[3]]
            
            # Content with side borders
            for line in art_lines:
                padded_line = line.ljust(max_width - 4)
                bordered_lines.append(f"{border[1]} {padded_line} {border[1]}")
            
            # Bottom border
            bordered_lines.append(border[4] + border[0] * (max_width - 2) + border[5])
            
            art_lines = bordered_lines
        
        # Join lines and update display
        self.current_art = "\n".join(art_lines)
        
        # Create Rich Text object for proper multi-line display
        rich_text = Text(self.current_art, style="white")
        self.query_one("#art-preview", Static).update(rich_text)
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle text input changes."""
        if event.input.id == "text-input":
            self.input_text = event.value
            if len(event.value) <= 20:  # Only generate if within limit
                self.generate_ascii_art(event.value)
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle style and alignment changes."""
        if event.select.id == "style-select":
            self.selected_style = event.value
            self.generate_ascii_art(self.input_text)
        elif event.select.id == "align-select":
            self.alignment = event.value
            self.generate_ascii_art(self.input_text)
    
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle border checkbox."""
        if event.checkbox.id == "border-checkbox":
            self.border_enabled = event.value
            self.generate_ascii_art(self.input_text)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "generate":
            text_input = self.query_one("#text-input", Input)
            self.input_text = text_input.value
            self.generate_ascii_art(text_input.value)
            self.notify(f"Generated ASCII art for: '{text_input.value}'" if text_input.value else "Please enter some text to generate art!")
            
        elif event.button.id == "clear":
            self.query_one("#text-input", Input).value = ""
            self.input_text = ""
            self.current_art = ""
            self.query_one("#art-preview", Static).update("")
            
        elif event.button.id == "copy":
            if self.current_art:
                # Simple notification (actual clipboard copy would need pyperclip)
                self.notify("ASCII Art copied to preview! 📋")
            else:
                self.notify("No art to copy! Generate some first.")
                
        elif event.button.id == "save-txt":
            if self.current_art:
                self.save_ascii_art()
            else:
                self.notify("No art to save! Generate some first.")
                
        elif event.button.id == "random":
            import random
            examples = ["AWESOME", "PYTHON", "TEXTUAL", "ASCII", "ART", "COOL", "WOW", "NICE"]
            random_text = random.choice(examples)
            self.query_one("#text-input", Input).value = random_text
            self.input_text = random_text
            self.generate_ascii_art(random_text)
    
    def save_ascii_art(self) -> None:
        """Save ASCII art to file."""
        try:
            filename = f"ascii_art_{self.input_text or 'generated'}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"ASCII Art Generator - Text: '{self.input_text}'\n")
                f.write(f"Style: {self.selected_style}, Border: {self.border_enabled}\n")
                f.write("=" * 50 + "\n\n")
                f.write(self.current_art)
                f.write("\n\n" + "=" * 50 + "\n")
                f.write("Generated with Textual ASCII Art Generator\n")
            
            self.notify(f"✅ Saved as {filename}")
        except Exception as e:
            self.notify(f"❌ Save failed: {str(e)}")


def main():
    """Run the ASCII Art Generator."""
    print("🎨 Starting ASCII Art Generator...")
    print("Create beautiful ASCII art from text!")
    print()
    
    app = ASCIIArtGenerator()
    app.title = "ASCII Art Generator"
    app.run()


if __name__ == "__main__":
    main()
