#!/usr/bin/env python3
"""
簡單的 Emoji 調試測試
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.containers import Vertical

class DebugEmoji(App):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("=== EMOJI DEBUG TEST ===", id="header")
            yield Static("", id="test-area")
            yield Button("Test Emoji", id="emoji-btn")
            yield Button("Test ASCII", id="ascii-btn")
            yield Button("Test Mixed", id="mixed-btn")
            yield Button("Exit", id="exit-btn")
    
    def on_mount(self):
        self.test_emoji()
    
    def test_emoji(self):
        emoji_text = "🐍 🍎 🟢 🟨 🔴 🌊 🚢 💥 💧 💀"
        self.query_one("#test-area").update(emoji_text)
        print(f"設置 emoji 文字: {emoji_text}")
    
    def test_ascii(self):
        ascii_text = "S @ O o # ~ S X o #"
        self.query_one("#test-area").update(ascii_text)
        print(f"設置 ASCII 文字: {ascii_text}")
    
    def test_mixed(self):
        mixed_text = "混合: 🐍S 🍎@ 🟢O 🟨o 🔴#"
        self.query_one("#test-area").update(mixed_text)
        print(f"設置混合文字: {mixed_text}")
    
    def on_button_pressed(self, event):
        if event.button.id == "emoji-btn":
            self.test_emoji()
        elif event.button.id == "ascii-btn":
            self.test_ascii()
        elif event.button.id == "mixed-btn":
            self.test_mixed()
        elif event.button.id == "exit-btn":
            self.exit()

if __name__ == "__main__":
    print("開始 Emoji 調試測試...")
    app = DebugEmoji()
    app.run()
