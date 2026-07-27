#!/usr/bin/env python3
"""
Textual Emoji 顯示測試
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Button
from textual.containers import Vertical, Horizontal

class EmojiTest(App):
    """Emoji 顯示測試"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    .emoji-grid {
        border: solid #444;
        background: #003366;
        margin: 1;
        padding: 1;
    }
    
    .emoji-cell {
        width: 4;
        height: 1;
        text-align: center;
        margin: 0 1;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("🧪 Emoji 顯示測試", id="title")
        yield Label("如果下方 emoji 顯示不正常，可能是終端或字體問題", id="info")
        
        with Vertical(classes="emoji-grid"):
            yield Label("基本 emoji:")
            with Horizontal():
                yield Static("😀", classes="emoji-cell")
                yield Static("😃", classes="emoji-cell") 
                yield Static("🎉", classes="emoji-cell")
                yield Static("❤️", classes="emoji-cell")
                yield Static("⭐", classes="emoji-cell")
            
            yield Label("遊戲相關 emoji:")
            with Horizontal():
                yield Static("🐍", classes="emoji-cell")
                yield Static("🍎", classes="emoji-cell")
                yield Static("🟢", classes="emoji-cell")
                yield Static("🟨", classes="emoji-cell")
                yield Static("🔴", classes="emoji-cell")
            
            yield Label("幾何符號:")
            with Horizontal():
                yield Static("●", classes="emoji-cell")
                yield Static("○", classes="emoji-cell")
                yield Static("■", classes="emoji-cell")
                yield Static("□", classes="emoji-cell")
                yield Static("▲", classes="emoji-cell")
            
            yield Label("ASCII 替代符號:")
            with Horizontal():
                yield Static("S", classes="emoji-cell")
                yield Static("@", classes="emoji-cell")
                yield Static("O", classes="emoji-cell")
                yield Static("#", classes="emoji-cell")
                yield Static("~", classes="emoji-cell")
        
        yield Button("退出 (Q)", id="quit")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.exit()
    
    def on_key(self, event) -> None:
        if event.key.lower() == "q":
            self.exit()

def main():
    app = EmojiTest()
    app.run()

if __name__ == "__main__":
    main()
