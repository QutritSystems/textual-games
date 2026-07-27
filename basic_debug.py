#!/usr/bin/env python3
"""
最基礎的 Textual 診斷程式
"""

import os
import sys
from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Button
from textual.containers import Vertical
from textual import events

class BasicDebug(App):
    """最基礎的診斷"""
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.test_widget = None
    
    def compose(self) -> ComposeResult:
        yield Label(f"Python: {sys.version}")
        yield Label(f"Terminal: {os.getenv('TERM', 'unknown')}")
        yield Label(f"Term Program: {os.getenv('TERM_PROGRAM', 'unknown')}")
        yield Label("=== 基礎測試 ===")
        
        self.test_widget = Static("初始內容")
        yield self.test_widget
        
        yield Button("更新內容", id="update")
        yield Button("退出", id="quit")
        yield Label("按任意鍵測試鍵盤...")
        yield Label("", id="key-display")
    
    def on_mount(self):
        """啟動時立即測試"""
        print("App 啟動成功")
        self.test_widget.update("🔥 如果你能看到這個火焰符號，說明 Unicode 正常")
        
        # 延遲測試
        self.set_timer(1.0, self.delayed_test)
        self.set_timer(2.0, lambda: self.test_widget.update("延遲2秒後的內容"))
        self.set_timer(3.0, lambda: self.test_widget.update("延遲3秒後的內容"))
    
    def delayed_test(self):
        """延遲測試"""
        print("執行延遲測試")
        self.test_widget.update("⭐ 延遲1秒後的內容")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update":
            self.counter += 1
            test_content = [
                f"更新 #{self.counter}",
                f"🎯 計數器: {self.counter}",
                f"📝 純文字 {self.counter}",
                f"Symbol: S-{self.counter}",
                f"ASCII: {chr(65 + (self.counter % 26))}"
            ]
            
            content = test_content[self.counter % len(test_content)]
            self.test_widget.update(content)
            print(f"更新內容為: {content}")
        
        elif event.button.id == "quit":
            print("退出程式")
            self.exit()
    
    def on_key(self, event: events.Key):
        """測試鍵盤輸入"""
        key_info = f"按鍵: {event.key} (code: {ord(event.key) if len(event.key) == 1 else 'multi'})"
        self.query_one("#key-display").update(key_info)
        print(key_info)
        
        if event.key.lower() == "q":
            self.exit()

def main():
    print("啟動基礎診斷程式...")
    app = BasicDebug()
    print("App 對象創建成功")
    app.run()

if __name__ == "__main__":
    main()
