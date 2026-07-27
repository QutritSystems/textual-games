#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
終端環境診斷腳本
檢查終端兼容性和 Textual 支持
"""

import os
import sys
from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.containers import Vertical

def check_environment():
    """檢查終端環境"""
    print("🔍 終端環境診斷")
    print("=" * 50)
    
    # 基本系統信息
    print(f"操作系統: {os.name}")
    print(f"Python 版本: {sys.version}")
    print(f"終端大小: {os.get_terminal_size()}")
    
    # 環境變數
    term = os.environ.get('TERM', '未設定')
    print(f"TERM: {term}")
    
    colorterm = os.environ.get('COLORTERM', '未設定')
    print(f"COLORTERM: {colorterm}")
    
    # 測試基本字符顯示
    print("\n📝 字符測試:")
    test_chars = [
        ("ASCII", "ABC123"),
        ("符號", "!@#$%"),
        ("框線", "┌─┐│└─┘"),
        ("表情", "🚢💥❌"),
        ("自定義", "[S] <X> ~~~ XXX")
    ]
    
    for name, chars in test_chars:
        print(f"  {name}: {chars}")
    
    print("\n" + "=" * 50)

class DiagnosticApp(App):
    """診斷應用"""
    
    CSS = """
    Screen {
        background: blue;
    }
    
    Static {
        color: white;
        background: red;
        margin: 1;
        padding: 1;
        border: solid white;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.test_static = None
        self.counter = 0
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("🔍 終端診斷測試", id="title")
            yield Static("初始文字", id="test")
            yield Button("測試更新", id="update-btn")
            yield Button("測試符號", id="symbol-btn") 
            yield Button("測試顏色", id="color-btn")
            yield Static("按 Q 退出", id="help")
    
    def on_mount(self):
        """初始化"""
        self.test_static = self.query_one("#test")
        self.query_one("#title").styles.background = "green"
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """按鈕處理"""
        if not self.test_static:
            return
            
        if event.button.id == "update-btn":
            self.counter += 1
            self.test_static.update(f"更新次數: {self.counter}")
            self.test_static.styles.background = ["red", "blue", "green", "yellow"][self.counter % 4]
            
        elif event.button.id == "symbol-btn":
            symbols = ["[S] 船隻", "<X> 命中", "~~~ 水域", "XXX 沉船"]
            symbol = symbols[self.counter % len(symbols)]
            self.test_static.update(symbol)
            
        elif event.button.id == "color-btn":
            colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
            color = colors[self.counter % len(colors)]
            self.test_static.styles.color = color

def main():
    """運行診斷"""
    check_environment()
    
    print("\n🚀 啟動 Textual 診斷應用...")
    print("如果你看到藍色背景和白色文字，說明基本渲染正常")
    print("嘗試點擊按鈕測試更新功能")
    print("按 Q 退出")
    
    app = DiagnosticApp()
    app.run()

if __name__ == "__main__":
    main()
