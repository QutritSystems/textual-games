#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Static widget display functionality
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Label, Button, Input, Header, Footer
from rich.text import Text


class StaticTestApp(App):
    """Test Static widget display."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .container {
        border: solid $primary;
        background: $panel;
        width: 80;
        margin: 2;
        padding: 2;
    }
    
    .test-display {
        background: $surface;
        color: $text;
        padding: 1;
        height: 15;
        border: solid $warning;
        margin: 1 0;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="container"):
            yield Label("Static Widget Display Test")
            
            yield Button("Test 1: Plain Text", id="test1", variant="primary")
            yield Button("Test 2: Rich Text", id="test2", variant="success")
            yield Button("Test 3: ASCII Art", id="test3", variant="warning")
            yield Button("Clear", id="clear", variant="error")
            
            yield Static("Ready for test...", id="display", classes="test-display")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize with test content."""
        self.test_ascii_art()
    
    def test_ascii_art(self):
        """Test ASCII art display."""
        ascii_art = """### ###  ### ### 
 #  #   #    # 
 #  ##   ### # 
 #  #      # # 
 #  ###  ### ###"""
        
        display = self.query_one("#display", Static)
        display.update(ascii_art)
        self.notify("ASCII art loaded!")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        display = self.query_one("#display", Static)
        
        if event.button.id == "test1":
            display.update("This is plain text test.\nLine 2\nLine 3")
            self.notify("Plain text test")
            
        elif event.button.id == "test2":
            rich_text = Text("Rich text test\nWith colors", style="bold blue")
            display.update(rich_text)
            self.notify("Rich text test")
            
        elif event.button.id == "test3":
            ascii_art = """####### #######  ###### ####### 
   ##   ##      ##         ##   
   ##   #####    #####     ##   
   ##   ##           ##    ##   
   ##   ####### ######     ##   """
            display.update(ascii_art)
            self.notify("ASCII art test")
            
        elif event.button.id == "clear":
            display.update("")
            self.notify("Cleared")


def main():
    """Run the test app."""
    print("🔍 Testing Static widget display...")
    print("Press buttons to test different display types.")
    
    app = StaticTestApp()
    app.title = "Static Display Test"
    app.run()


if __name__ == "__main__":
    main()
