#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決文字版本 - 使用文字字符而不是表情符號
解決表情符號顯示問題
"""

from battleship_game import *

# 重新定義 CellState 使用文字字符
class TextCellState(Enum):
    """網格單元狀態 - 文字版本"""
    EMPTY = " . "      # 空白水域
    SHIP = " S "       # 船隻 (Ship)
    HIT = " X "        # 命中 (Hit)
    MISS = " O "       # 未命中 (Miss)
    SUNK = " # "       # 沉船 (Sunk)

class TextBattleshipGame(BattleshipGame):
    """文字版潛艇對決遊戲"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    GridCell {
        width: 4;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: solid white;
        color: white;
        background: #003366;
    }
    
    GridCell:hover {
        background: #004466;
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
    
    #placement-title {
        text-style: bold;
        color: #FFD700;
    }
    
    Button {
        margin: 1;
    }
    
    Label {
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素 - 使用文字版本"""
        yield Label("*** 潛艇對決 BATTLESHIP GAME *** [文字版]", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家區域
            with Vertical():
                self.player_grid = TextGameGrid(self.player_board, "*** 你的戰場 ***", clickable=True, show_ships=True)
                yield self.player_grid
            
            # 控制面板
            yield self.placement_panel
            
            # AI 區域  
            with Vertical():
                self.ai_grid = TextGameGrid(self.ai_board, "*** 敵方戰場 ***", clickable=False, show_ships=False)
                yield self.ai_grid
    
    def on_mount(self):
        """應用啟動時的初始化"""
        super().on_mount()
        # 立即放置測試船隻
        self.set_timer(0.5, self.place_test_ships)
    
    def place_test_ships(self):
        """放置測試船隻"""
        print("🔧 放置測試船隻...")
        
        # 為玩家放置測試船隻
        test_ship = Ship("測試船", 3)
        if self.player_board.place_ship(test_ship, 1, 1, Orientation.HORIZONTAL):
            print("✅ 玩家測試船放置成功")
            # 強制更新網格
            if self.player_grid:
                self.player_grid.update_grid()
        
        # 確保AI網格也更新
        if self.ai_grid:
            self.ai_grid.update_grid()
        
        self.update_status("測試船隻已放置！圖例: . = 空水域, S = 船隻, X = 命中, O = 未命中, # = 沉船")

class TextGameGrid(GameGrid):
    """文字版遊戲網格"""
    
    def update_grid(self):
        """更新網格顯示 - 使用文字狀態"""
        print(f"🔄 更新文字網格: {self.title}")
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                # 取得棋盤狀態
                board_state = self.board.grid[row][col]
                
                # 轉換為文字狀態
                if board_state == CellState.EMPTY:
                    text_state = TextCellState.EMPTY
                elif board_state == CellState.SHIP:
                    text_state = TextCellState.SHIP if self.show_ships else TextCellState.EMPTY
                elif board_state == CellState.HIT:
                    text_state = TextCellState.HIT
                elif board_state == CellState.MISS:
                    text_state = TextCellState.MISS
                elif board_state == CellState.SUNK:
                    text_state = TextCellState.SUNK
                else:
                    text_state = TextCellState.EMPTY
                
                # 更新單元格顯示
                if row < len(self.cells) and col < len(self.cells[row]):
                    self.cells[row][col].update(text_state.value)
                    
                    # 調試前3x3區域
                    if row < 3 and col < 3:
                        print(f"  文字格子({row},{col}): {board_state.name} -> 顯示 '{text_state.value}'")

def main():
    """運行文字版本"""
    print("📝 啟動潛艇對決文字版本...")
    print("使用文字字符代替表情符號:")
    print("  . = 空水域")
    print("  S = 船隻")
    print("  X = 命中")
    print("  O = 未命中")
    print("  # = 沉船")
    print()
    
    app = TextBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
