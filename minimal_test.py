#!/usr/bin/env python3
"""
最簡單的 Textual 測試
"""

import os
import sys
from textual.app import App, ComposeResult
from textual.widgets import Static

print(f"Python: {sys.version}")
print(f"Textual 模組位置: {__import__('textual').__file__}")
print(f"終端: {os.getenv('TERM_PROGRAM', 'unknown')}")
print("="*50)

class MinimalApp(App):
    """最簡單的應用"""
    
    def compose(self) -> ComposeResult:
        print("compose() 被調用")
        yield Static("Hello World!")
        print("Static 組件已產生")
    
    def on_mount(self):
        print("on_mount() 被調用")
        print("應用已掛載")

def main():
    print("創建應用...")
    app = MinimalApp()
    print("開始運行...")
    try:
        app.run()
    except Exception as e:
        print(f"運行錯誤: {e}")
        import traceback
        traceback.print_exc()
    print("應用結束")

if __name__ == "__main__":
    main()
