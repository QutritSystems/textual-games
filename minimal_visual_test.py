#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化視覺效果測試
直接測試 Textual 的 Static 組件更新
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Label
from textual import events

class MinimalVisualTest(App):
    """最小化視覺測試應用"""
    
    def __init__(self):
        super().__init__()
        self.test_cells = []
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素"""
        yield Label("🔍 視覺效果測試", id="title")
        yield Label("點擊按鈕測試表情符號顯示", id="status")
        
        with Horizontal():
            # 測試網格
            with Vertical():
                yield Label("測試網格:")
                with Horizontal():
                    for i in range(3):
                        cell = Static("⬜", id=f"cell-{i}")
                        self.test_cells.append(cell)
                        yield cell
            
            # 控制按鈕
            with Vertical():
                yield Button("顯示船隻 🚢", id="ship-btn")
                yield Button("顯示命中 💥", id="hit-btn")
                yield Button("顯示未命中 ❌", id="miss-btn")
                yield Button("顯示沉船 💀", id="sunk-btn")
                yield Button("重置 ⬜", id="reset-btn")
    
    def on_mount(self):
        """初始化"""
        self.query_one("#status").update("✅ 應用已加載，嘗試點擊按鈕")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """處理按鈕點擊"""
        if not self.test_cells:
            self.query_one("#status").update("❌ 測試單元格未找到")
            return
            
        if event.button.id == "ship-btn":
            self.test_cells[0].update("🚢")
            self.query_one("#status").update("設置第1格為船隻")
            
        elif event.button.id == "hit-btn":
            self.test_cells[1].update("💥")
            self.query_one("#status").update("設置第2格為命中")
            
        elif event.button.id == "miss-btn":
            self.test_cells[2].update("❌")
            self.query_one("#status").update("設置第3格為未命中")
            
        elif event.button.id == "sunk-btn":
            for cell in self.test_cells:
                cell.update("💀")
            self.query_one("#status").update("設置所有格為沉船")
            
        elif event.button.id == "reset-btn":
            for cell in self.test_cells:
                cell.update("⬜")
            self.query_one("#status").update("重置所有格子")
    
    def on_key(self, event: events.Key) -> None:
        """鍵盤快捷鍵"""
        if event.key == "q":
            self.exit()

def main():
    """運行最小化測試"""
    print("🔍 啟動最小化視覺效果測試...")
    print("📝 這個測試會:")
    print("  - 顯示3個測試格子")
    print("  - 點擊按鈕更新格子內容")
    print("  - 檢查表情符號是否正常顯示")
    print("  - 按 Q 退出")
    print()
    
    app = MinimalVisualTest()
    app.run()

if __name__ == "__main__":
    main()
