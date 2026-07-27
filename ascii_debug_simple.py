#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra-simple ASCII generator with debug output
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Label, Button, Header, Footer


class DebugASCIIApp(App):
    """Debug ASCII display."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .main {
        border: solid $primary;
        width: 80;
        margin: 2;
        padding: 2;
    }
    
    .display {
        background: $surface;
        color: $text;
        padding: 2;
        height: 12;
        border: solid $success;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="main"):
            yield Label("ASCII Debug Test")
            yield Button("Show ASCII", id="show", variant="primary")
            yield Static("Click button to show ASCII art", id="display", classes="display")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Show ASCII art."""
        if event.button.id == "show":
            # Very simple ASCII art
            art = """##   ## ####### ##      ##       ###### 
##   ## ##      ##      ##      ##    ##
####### #####   ##      ##      ##    ##
##   ## ##      ##      ##      ##    ##
##   ## ####### ####### #######  ###### """
            
            display = self.query_one("#display", Static)
            display.update(art)
            
            # Debug notifications
            self.notify("ASCII art updated!")
            print(f"Debug: Art has {len(art)} characters")
            print(f"Debug: Art has {art.count(chr(10)) + 1} lines")


if __name__ == "__main__":
    print("🔧 Debug: Ultra-simple ASCII test")
    app = DebugASCIIApp()
    app.run()
