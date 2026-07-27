#!/usr/bin/env python3
"""
強制刷新版潛艇對決
使用更激進的顯示方法
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Label
from textual.reactive import reactive
from textual import events
from textual.message import Message
import random
import time

class ForceCell(Static):
    """強制刷新的格子"""
    
    def __init__(self, row: int, col: int, symbol: str = "~"):
        super().__init__(symbol)
        self.row = row
        self.col = col
        self.current_symbol = symbol
    
    def force_set(self, symbol: str, color: str = "white"):
        """強制設置內容和顏色"""
        self.current_symbol = symbol
        
        # 多重刷新確保顯示
        self.update(symbol)
        self.renderable = symbol
        self.styles.color = color
        self.refresh()
        
        # 強制重新渲染
        self.app.call_later(lambda: self.update(symbol))
    
    def on_click(self) -> None:
        """點擊事件"""
        self.post_message(CellClicked(self.row, self.col))

class CellClicked(Message):
    """格子點擊訊息"""
    def __init__(self, row: int, col: int):
        super().__init__()
        self.row = row
        self.col = col

class ForceDisplayGame(App):
    """強制顯示版遊戲"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    ForceCell {
        width: 4;
        height: 1;
        text-align: center;
        border: solid #666;
        background: #003366;
        color: white;
        margin: 0;
        padding: 0;
    }
    
    ForceCell:hover {
        background: #006699;
    }
    
    #status {
        background: #330033;
        color: #FFFF00;
        text-align: center;
        padding: 1;
        margin: 1;
    }
    
    Button {
        margin: 1;
        background: #006600;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.grid_size = 5  # 簡化為 5x5
        self.cells = []
        self.counter = 0
        self.status_widget = None
    
    def compose(self) -> ComposeResult:
        yield Label("🎯 強制顯示測試版", id="title")
        
        self.status_widget = Label("點擊格子測試顯示效果", id="status")
        yield self.status_widget
        
        # 簡化的 5x5 網格
        with Container(id="game-area"):
            for row in range(self.grid_size):
                grid_row = []
                with Horizontal():
                    for col in range(self.grid_size):
                        cell = ForceCell(row, col, "~")
                        grid_row.append(cell)
                        yield cell
                self.cells.append(grid_row)
        
        with Horizontal():
            yield Button("隨機放置", id="random")
            yield Button("清空", id="clear")
            yield Button("測試動畫", id="animate")
            yield Button("退出", id="quit")
    
    def on_mount(self):
        """初始化"""
        self.update_status("遊戲已啟動 - 網格初始化完成")
        
        # 延遲放置一些測試內容
        self.set_timer(1.0, self.initial_test)
    
    def initial_test(self):
        """初始測試內容"""
        test_positions = [(1, 1), (1, 2), (2, 1), (3, 3)]
        symbols = ["S", "X", "o", "#"]
        colors = ["green", "red", "blue", "yellow"]
        
        for (row, col), symbol, color in zip(test_positions, symbols, colors):
            if row < self.grid_size and col < self.grid_size:
                self.cells[row][col].force_set(symbol, color)
        
        self.update_status("已放置測試符號 - 如果看不到請點擊按鈕測試")
    
    def update_status(self, message: str):
        """更新狀態"""
        if self.status_widget:
            self.status_widget.update(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def on_cell_clicked(self, message: CellClicked):
        """處理格子點擊"""
        row, col = message.row, message.col
        
        # 循環切換符號
        symbols = ["~", "S", "X", "o", "#"]
        colors = ["white", "green", "red", "blue", "yellow"]
        
        current = self.cells[row][col].current_symbol
        try:
            current_index = symbols.index(current)
            next_index = (current_index + 1) % len(symbols)
        except ValueError:
            next_index = 0
        
        new_symbol = symbols[next_index]
        new_color = colors[next_index]
        
        self.cells[row][col].force_set(new_symbol, new_color)
        self.update_status(f"點擊 ({row},{col}) -> {new_symbol}")
    
    async def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        
        if button_id == "random":
            self.counter += 1
            symbols = ["S", "X", "o", "#", "~"]
            colors = ["green", "red", "blue", "yellow", "white"]
            
            # 隨機更新5個格子
            positions = []
            for _ in range(5):
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                positions.append((row, col))
            
            for row, col in positions:
                symbol = random.choice(symbols)
                color = random.choice(colors)
                self.cells[row][col].force_set(symbol, color)
            
            self.update_status(f"隨機更新 #{self.counter} - 已更新 {len(positions)} 個格子")
        
        elif button_id == "clear":
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    self.cells[row][col].force_set("~", "white")
            self.update_status("已清空所有格子")
        
        elif button_id == "animate":
            await self.run_animation()
        
        elif button_id == "quit":
            self.exit()
    
    async def run_animation(self):
        """運行動畫測試"""
        self.update_status("開始動畫測試...")
        
        for i in range(10):
            row = i % self.grid_size
            col = (i * 2) % self.grid_size
            
            # 設置符號
            self.cells[row][col].force_set("*", "yellow")
            self.update_status(f"動畫步驟 {i+1}/10")
            
            # 等待
            import asyncio
            await asyncio.sleep(0.5)
            
            # 恢復
            self.cells[row][col].force_set("~", "white")
        
        self.update_status("動畫測試完成")
    
    def on_key(self, event: events.Key):
        if event.key.lower() == "q":
            self.exit()

def main():
    print("啟動強制顯示版遊戲...")
    app = ForceDisplayGame()
    app.run()

if __name__ == "__main__":
    main()
