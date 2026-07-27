#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決 Emoji 版本
使用與 final_battleship 相同的結構，但用 emoji 符號測試你的理論
"""

from final_battleship import *

# 重新定義符號為 emoji 版本
class EmojiCellState(Enum):
    """網格單元狀態 - Emoji 版本"""
    EMPTY = "🌊"      # 海水
    SHIP = "🚢"       # 船隻
    HIT = "💥"        # 命中
    MISS = "💧"       # 未命中
    SUNK = "💀"       # 沉船

class EmojiGridCell(FinalGridCell):
    """Emoji 版本網格單元"""
    
    def __init__(self, row: int, col: int, clickable: bool = True):
        super().__init__(row, col, clickable)
        # 初始化時設置為海水
        self.update("🌊")
    
    def set_display(self, state: CellState):
        """設置顯示內容 - 轉換為 emoji"""
        self.cell_state = state
        
        # 將基本狀態轉換為 emoji
        if state == CellState.EMPTY:
            emoji_symbol = "🌊"
            color = "blue"
        elif state == CellState.SHIP:
            emoji_symbol = "🚢"
            color = "green"
        elif state == CellState.HIT:
            emoji_symbol = "💥"
            color = "red"
        elif state == CellState.MISS:
            emoji_symbol = "💧"
            color = "blue"
        elif state == CellState.SUNK:
            emoji_symbol = "💀"
            color = "yellow"
        else:
            emoji_symbol = "❓"
            color = "white"
        
        # 更新顯示
        self.update(emoji_symbol)
        self.styles.color = color

class EmojiGameGrid(FinalGameGrid):
    """Emoji 版本遊戲網格"""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.title)
            with Container(id="grid-container"):
                for row in range(self.board.size):
                    cell_row = []
                    with Horizontal():
                        for col in range(self.board.size):
                            # 使用 EmojiGridCell 替代 FinalGridCell
                            cell = EmojiGridCell(row, col, self.clickable)
                            cell_row.append(cell)
                            yield cell
                    self.cells.append(cell_row)

class EmojiBattleshipGame(FinalBattleshipGame):
    """Emoji 版潛艇對決遊戲"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    EmojiGridCell {
        width: 3;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: solid #444;
        background: #003366;
    }
    
    EmojiGridCell:hover {
        background: #006699;
    }
    
    #grid-container {
        border: solid white;
        margin: 1;
        padding: 1;
    }
    
    #game-title {
        text-align: center;
        text-style: bold;
        color: #FFD700;
        margin: 1;
    }
    
    #game-status {
        text-align: center;
        color: #00FF00;
        margin: 1;
    }
    
    Button {
        margin: 1;
    }
    
    Label {
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("🚢 潛艇對決 🚢 [EMOJI 測試版]", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家戰場
            with Vertical():
                self.player_grid = EmojiGameGrid(self.player_board, "🏴‍☠️ 你的戰場", True, True)
                yield self.player_grid
            
            # 控制面板
            with Vertical():
                yield Label("⚙️ 控制面板", id="panel-title")
                yield Label("", id="current-ship")
                yield Button("🔄 切換方向", id="rotate")
                yield Button("🎯 自動放置", id="auto-place")
                yield Button("⚔️ 開始戰鬥", id="start-battle", disabled=True)
                yield Label("", id="legend")
            
            # AI 戰場
            with Vertical():
                self.ai_grid = EmojiGameGrid(self.ai_board, "🤖 敵方戰場", False, False)
                yield self.ai_grid
    
    def on_mount(self):
        """初始化"""
        self.update_status("點擊你的戰場放置船隻")
        self.update_ship_info()
        self.query_one("#legend").update("符號: 🌊 海水, 🚢 船隻, 💥 命中, 💧 未命中, 💀 沉船")
        
        # 自動放置測試船隻
        self.set_timer(1.0, self.demo_place_ship)

def main():
    print("🚢 啟動 Emoji 版潛艇對決...")
    print("這個版本使用 emoji 符號測試網格顯示:")
    print("  🌊 = 海水")
    print("  🚢 = 船隻") 
    print("  💥 = 命中")
    print("  💧 = 未命中")
    print("  💀 = 沉船")
    print()
    
    app = EmojiBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
