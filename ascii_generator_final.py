#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCII Art Generator - Final Version with Display Fixes
"""

import random
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Label, Button, Input, Header, Footer, Select, Checkbox
from textual.reactive import reactive


class ASCIIArtGenerator(App):
    """Final ASCII Art Generator with guaranteed display."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .container {
        border: solid $primary;
        background: $panel;
        width: 95;
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
    
    .input-area {
        border: solid $accent;
        background: $surface;
        margin: 1 0;
        padding: 1;
    }
    
    .preview-container {
        border: solid $success;
        background: $panel;
        margin: 1 0;
        padding: 1;
        height: 30;
    }
    
    .art-display {
        background: black;
        color: white;
        padding: 1;
        height: 25;
        border: solid cyan;
    }
    
    .controls {
        margin: 1 0;
        padding: 1;
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
    """
    
    input_text = reactive("")
    selected_style = reactive("Big")
    border_enabled = reactive(False)
    alignment = reactive("left")
    
    def __init__(self):
        super().__init__()
        
        # Simple ASCII fonts
        self.fonts = {
            "Big": {
                'A': ["  ##  ", " #  # ", "#####", "#    #", "#    #"],
                'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
                'C': [" ### ", "#   ", "#    ", "#    ", " ### "],
                'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
                'E': ["#####", "#    ", "#### ", "#    ", "#####"],
                'F': ["#####", "#    ", "#### ", "#    ", "#    "],
                'G': [" ### ", "#    ", "# ## ", "#  # ", " ### "],
                'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
                'I': ["#####", "  #  ", "  #  ", "  #  ", "#####"],
                'J': ["#####", "    #", "    #", "#   #", " ### "],
                'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
                'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
                'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
                'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
                'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
                'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
                'Q': [" ### ", "#   #", "# # #", "#  ##", " ####"],
                'R': ["#### ", "#   #", "#### ", "#   #", "#   #"],
                'S': [" ### ", "#    ", " ### ", "    #", " ### "],
                'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
                'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
                'V': ["#   #", "#   #", "#   #", " # # ", "  #  "],
                'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
                'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
                'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
                'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
                ' ': ["     ", "     ", "     ", "     ", "     "],
                '!': ["  #  ", "  #  ", "  #  ", "     ", "  #  "],
                '?': [" ### ", "   # ", "  ## ", "     ", "  #  "],
            },
            
            "Block": {
                'A': ["██", "██", "██"],
                'B': ["██", "██", "██"],
                'C': ["██", "█ ", "██"],
                'D': ["██", "██", "██"],
                'E': ["██", "█ ", "██"],
                'F': ["██", "█ ", "█ "],
                'G': ["██", "██", "██"],
                'H': ["██", "██", "██"],
                'I': ["█", "█", "█"],
                'J': ["██", " █", "██"],
                'K': ["██", "█ ", "██"],
                'L': ["█ ", "█ ", "██"],
                'M': ["███", "███", "█ █"],
                'N': ["██", "██", "██"],
                'O': ["██", "██", "██"],
                'P': ["██", "█ ", "█ "],
                'Q': ["██", "██", "██"],
                'R': ["██", "██", "██"],
                'S': ["██", " █", "██"],
                'T': ["███", " █ ", " █ "],
                'U': ["██", "██", "██"],
                'V': ["██", "██", " █"],
                'W': ["███", "███", "███"],
                'X': ["██", " █", "██"],
                'Y': ["██", " █", " █"],
                'Z': ["██", " █", "██"],
                ' ': ["  ", "  ", "  "],
                '!': ["█", "█", "█"],
                '?': ["█", "█", "█"],
            },
            
            "Small": {
                'A': ["#", "#", "#"],
                'B': ["#", "#", "#"],
                'C': ["#", "#", "#"],
                'D': ["#", "#", "#"],
                'E': ["#", "#", "#"],
                'F': ["#", "#", "#"],
                'G': ["#", "#", "#"],
                'H': ["#", "#", "#"],
                'I': ["#", "#", "#"],
                'J': ["#", "#", "#"],
                'K': ["#", "#", "#"],
                'L': ["#", "#", "#"],
                'M': ["#", "#", "#"],
                'N': ["#", "#", "#"],
                'O': ["#", "#", "#"],
                'P': ["#", "#", "#"],
                'Q': ["#", "#", "#"],
                'R': ["#", "#", "#"],
                'S': ["#", "#", "#"],
                'T': ["#", "#", "#"],
                'U': ["#", "#", "#"],
                'V': ["#", "#", "#"],
                'W': ["#", "#", "#"],
                'X': ["#", "#", "#"],
                'Y': ["#", "#", "#"],
                'Z': ["#", "#", "#"],
                ' ': [" ", " ", " "],
                '!': ["#", "#", "#"],
                '?': ["#", "#", "#"],
            }
        }
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="container"):
            yield Static("🎨 ASCII ART GENERATOR 🎨", classes="title")
            
            # Input section
            with Container(classes="input-area"):
                yield Label("Enter Text (max 8 chars):")
                yield Input(placeholder="Type here...", id="text-input", max_length=8)
            
            # Controls
            with Container(classes="controls"):
                with Horizontal():
                    yield Select([
                        ("Big Font", "Big"),
                        ("Block Font", "Block"), 
                        ("Small Font", "Small")
                    ], value="Big", id="style-select")
                    
                    yield Checkbox("Border", id="border-checkbox")
                    
                    yield Button("Generate", id="generate", variant="primary")
                    yield Button("Clear", id="clear", variant="warning")
                    yield Button("Random", id="random", variant="success")
            
            # Preview section - ENLARGED
            with Container(classes="preview-container"):
                yield Label("ASCII Art Preview:")
                yield Static("Enter text above to generate ASCII art!", id="art-display", classes="art-display")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize with test."""
        self.input_text = "TEST"
        self.query_one("#text-input", Input).value = "TEST"
        self.generate_art("TEST")
    
    def generate_art(self, text: str) -> None:
        """Generate ASCII art."""
        if not text:
            self.query_one("#art-display", Static).update("Enter text to generate ASCII art!")
            return
        
        text = text.upper()[:8]
        font = self.fonts.get(self.selected_style, self.fonts["Big"])
        
        # Get font height
        font_height = len(list(font.values())[0])
        
        # Generate lines
        lines = [""] * font_height
        
        for char in text:
            if char in font:
                char_lines = font[char]
                for i in range(font_height):
                    lines[i] += char_lines[i] + " "
        
        # Add border if enabled
        if self.border_enabled:
            max_width = max(len(line) for line in lines) + 4
            bordered = ["+" + "-" * (max_width - 2) + "+"]
            for line in lines:
                bordered.append(f"| {line.ljust(max_width - 4)} |")
            bordered.append("+" + "-" * (max_width - 2) + "+")
            lines = bordered
        
        # Join and display
        art = "\n".join(lines)
        
        # Force update
        display = self.query_one("#art-display", Static)
        display.update(art)
        
        # Debug notification
        self.notify(f"Generated '{text}' - {len(lines)} lines")
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "text-input":
            self.input_text = event.value
            if event.value and len(event.value) <= 8:
                self.generate_art(event.value)
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle style changes."""
        if event.select.id == "style-select":
            self.selected_style = event.value
            if self.input_text:
                self.generate_art(self.input_text)
    
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle border checkbox."""
        if event.checkbox.id == "border-checkbox":
            self.border_enabled = event.value
            if self.input_text:
                self.generate_art(self.input_text)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle buttons."""
        if event.button.id == "generate":
            text = self.query_one("#text-input", Input).value
            if text:
                self.input_text = text
                self.generate_art(text)
            else:
                self.notify("Enter some text first!")
        
        elif event.button.id == "clear":
            self.query_one("#text-input", Input).value = ""
            self.query_one("#art-display", Static).update("Enter text to generate ASCII art!")
            self.input_text = ""
        
        elif event.button.id == "random":
            words = ["HELLO", "WORLD", "ASCII", "ART", "TEST", "COOL", "WOW", "YES"]
            word = random.choice(words)
            self.query_one("#text-input", Input).value = word
            self.input_text = word
            self.generate_art(word)


def main():
    """Run the app."""
    print("🎨 ASCII Art Generator - Final Version")
    print("This version should definitely show ASCII art!")
    
    app = ASCIIArtGenerator()
    app.title = "ASCII Art Generator - Final"
    app.run()


if __name__ == "__main__":
    main()
