#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Test ASCII Art Generator - with debug output
"""

import random
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Label, Button, Input, Header, Footer, Select, Checkbox
from textual.reactive import reactive
from rich.text import Text


class SimpleASCIIApp(App):
    """Simple ASCII Art Generator for manual testing."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .container {
        border: solid $primary;
        background: $panel;
        width: 90;
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
    
    .preview-area {
        border: solid $success;
        background: $panel;
        margin: 1 0;
        padding: 1;
        height: 25;
    }
    
    .art-display {
        background: $surface;
        color: $text;
        padding: 1;
        height: 20;
        border: solid $warning;
    }
    
    Button {
        margin: 0 1;
    }
    
    Input {
        margin: 1 0;
        width: 100%;
    }
    """
    
    input_text = reactive("")
    
    def __init__(self):
        super().__init__()
        # Simple font for testing
        self.font = {
            'A': ["###", "#*#", "###", "# #", "# #"],
            'B': ["## ", "#*#", "## ", "#*#", "## "],
            'C': ["###", "#  ", "#  ", "#  ", "###"],
            'D': ["## ", "# #", "# #", "# #", "## "],
            'E': ["###", "#  ", "## ", "#  ", "###"],
            'F': ["###", "#  ", "## ", "#  ", "#  "],
            'G': ["###", "#  ", "#*#", "# #", "###"],
            'H': ["# #", "# #", "###", "# #", "# #"],
            'I': ["###", " # ", " # ", " # ", "###"],
            'J': ["###", "  #", "  #", "# #", "###"],
            'K': ["# #", "## ", "#* ", "# #", "# #"],
            'L': ["#  ", "#  ", "#  ", "#  ", "###"],
            'M': ["###", "###", "#*#", "# #", "# #"],
            'N': ["###", "# #", "# #", "# #", "# #"],
            'O': ["###", "# #", "# #", "# #", "###"],
            'P': ["## ", "# #", "## ", "#  ", "#  "],
            'Q': ["###", "# #", "#*#", "#*#", "###"],
            'R': ["## ", "# #", "## ", "# #", "# #"],
            'S': ["###", "#  ", "###", "  #", "###"],
            'T': ["###", " # ", " # ", " # ", " # "],
            'U': ["# #", "# #", "# #", "# #", "###"],
            'V': ["# #", "# #", "# #", "*#*", " # "],
            'W': ["# #", "# #", "#*#", "###", "###"],
            'X': ["# #", "*#*", " # ", "*#*", "# #"],
            'Y': ["# #", "*#*", " # ", " # ", " # "],
            'Z': ["###", " # ", " # ", " # ", "###"],
            ' ': ["   ", "   ", "   ", "   ", "   "],
            '!': [" # ", " # ", " # ", "   ", " # "],
            '?': ["## ", " # ", " # ", "   ", " # "],
        }
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="container"):
            yield Static("🎨 ASCII ART TEST 🎨", classes="title")
            
            # Input section
            with Container(classes="input-area"):
                yield Label("Enter Text (max 8 chars):")
                yield Input(placeholder="Type here...", id="text-input", max_length=8)
                yield Button("Generate", id="generate", variant="primary")
                yield Button("Test", id="test", variant="success")
            
            # Preview section
            with Container(classes="preview-area"):
                yield Label("ASCII Art Preview:")
                yield Static("Ready to generate ASCII art...", id="art-display", classes="art-display")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize with test text."""
        self.input_text = "TEST"
        self.query_one("#text-input", Input).value = "TEST"
        self.generate_art("TEST")
    
    def generate_art(self, text: str) -> None:
        """Generate simple ASCII art."""
        if not text:
            self.query_one("#art-display", Static).update("Enter some text to generate art!")
            return
        
        text = text.upper()[:8]
        art_lines = [""] * 5
        
        for char in text:
            if char in self.font:
                char_lines = self.font[char]
                for i in range(5):
                    art_lines[i] += char_lines[i] + " "
        
        # Join and display
        ascii_art = "\n".join(art_lines)
        
        # Create Rich Text and update
        rich_text = Text(ascii_art, style="bright_white")
        self.query_one("#art-display", Static).update(rich_text)
        
        # Debug output
        self.notify(f"Generated art for: '{text}' ({len(ascii_art)} chars)")
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle text input changes."""
        if event.input.id == "text-input":
            self.input_text = event.value
            if len(event.value) <= 8:
                self.generate_art(event.value)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "generate":
            text_input = self.query_one("#text-input", Input)
            self.generate_art(text_input.value)
            
        elif event.button.id == "test":
            test_words = ["HELLO", "TEST", "ASCII", "OK", "WOW"]
            test_word = random.choice(test_words)
            self.query_one("#text-input", Input).value = test_word
            self.input_text = test_word
            self.generate_art(test_word)


def main():
    """Run the test app."""
    print("🎨 Starting ASCII Art Test...")
    print("This should show ASCII art in the preview area.")
    print()
    
    app = SimpleASCIIApp()
    app.title = "ASCII Art Test"
    app.run()


if __name__ == "__main__":
    main()
