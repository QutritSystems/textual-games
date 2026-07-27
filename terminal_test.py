#!/usr/bin/env python3
"""
簡單的 Textual 終端相容性測試
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static, Label

class TerminalTest(App):
    """終端相容性測試"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    .test-cell {
        width: 3;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: solid #444;
        background: #003366;
        color: white;
    }
    
    .test-cell.red {
        background: red;
        color: white;
    }
    
    .test-cell.green {
        background: green;
        color: white;
    }
    
    .test-cell.blue {
        background: blue;
        color: white;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.test_cells = []
    
    def compose(self) -> ComposeResult:
        yield Label("🧪 終端相容性測試", id="title")
        yield Label("如果你能看到這行文字和下面的彩色格子，說明終端支援 Textual", id="status")
        
        # 測試網格
        with Vertical():
            for row in range(3):
                with Horizontal():
                    for col in range(5):
                        cell = Static("~", classes="test-cell")
                        self.test_cells.append(cell)
                        yield cell
        
        yield Button("測試更新", id="test-update")
        yield Button("退出 (Q)", id="quit")
    
    def on_mount(self):
        """初始化時設置一些測試內容"""
        self.call_later(self.initial_test)
    
    def initial_test(self):
        """設置初始測試內容"""
        # 設置一些測試符號和顏色
        test_patterns = [
            ("S", "green"), ("X", "red"), ("o", "blue"),
            ("#", "red"), ("~", ""), ("S", "green"),
            ("X", "red"), ("o", "blue"), ("#", "red"),
            ("~", ""), ("S", "green"), ("X", "red"),
            ("o", "blue"), ("#", "red"), ("~", "")
        ]
        
        for i, (symbol, color) in enumerate(test_patterns):
            if i < len(self.test_cells):
                cell = self.test_cells[i]
                cell.update(symbol)
                if color:
                    cell.add_class(color)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "test-update":
            self.counter += 1
            # 隨機更新一些格子
            import random
            symbols = ["S", "X", "o", "#", "~"]
            colors = ["", "red", "green", "blue"]
            
            for _ in range(5):  # 更新5個隨機格子
                cell = random.choice(self.test_cells)
                symbol = random.choice(symbols)
                color = random.choice(colors)
                
                # 清除所有顏色類
                cell.remove_class("red")
                cell.remove_class("green") 
                cell.remove_class("blue")
                
                cell.update(symbol)
                if color:
                    cell.add_class(color)
            
            self.query_one("#status").update(f"更新了 {self.counter} 次 - 格子應該會改變顏色和符號")
        
        elif event.button.id == "quit":
            self.exit()
    
    def on_key(self, event) -> None:
        if event.key.lower() == "q":
            self.exit()

def main():
    app = TerminalTest()
    app.run()

if __name__ == "__main__":
    main()
