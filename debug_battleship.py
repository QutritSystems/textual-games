#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決調試版本 - 添加詳細的視覺效果調試信息
"""

from battleship_game import *

class DebugGridCell(GridCell):
    """調試版網格單元"""
    
    def set_state(self, state: CellState):
        """設置單元狀態 - 添加調試信息"""
        print(f"🔧 GridCell ({self.row},{self.col}) 狀態變更: {self.state.name} -> {state.name} ({state.value})")
        super().set_state(state)

class DebugGameGrid(GameGrid):
    """調試版遊戲網格"""
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素 - 使用調試版本的 GridCell"""
        with Vertical():
            yield Label(self.title)
            for row in range(self.board.size):
                cell_row = []
                with Horizontal():
                    for col in range(self.board.size):
                        # 使用調試版本的 GridCell
                        cell = DebugGridCell(row, col, CellState.EMPTY, self.clickable)
                        cell_row.append(cell)
                        yield cell
                self.cells.append(cell_row)
    
    def update_grid(self):
        """更新網格顯示 - 添加調試信息"""
        print(f"🔄 更新網格: {self.title}")
        print(f"   show_ships={self.show_ships}")
        
        for row in range(min(3, self.board.size)):  # 只顯示前3行的調試信息
            for col in range(min(3, self.board.size)):  # 只顯示前3列
                cell_state = self.board.grid[row][col]
                
                if not self.show_ships and cell_state == CellState.SHIP:
                    display_state = CellState.EMPTY
                    print(f"   ({row},{col}): {cell_state.name} -> 隱藏為 {display_state.name}")
                else:
                    display_state = cell_state
                    print(f"   ({row},{col}): {cell_state.name} -> 顯示為 {display_state.name}")
                
                self.cells[row][col].set_state(display_state)
        
        # 更新剩餘的格子（不輸出調試信息）
        for row in range(self.board.size):
            for col in range(self.board.size):
                if row >= 3 or col >= 3:  # 跳過已經處理的前3x3區域
                    cell_state = self.board.grid[row][col]
                    if not self.show_ships and cell_state == CellState.SHIP:
                        display_state = CellState.EMPTY
                    else:
                        display_state = cell_state
                    self.cells[row][col].set_state(display_state)

class DebugBattleshipGame(BattleshipGame):
    """調試版潛艇對決遊戲"""
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素 - 使用調試版本的網格"""
        yield Label("🚢 潛艇對決 BATTLESHIP GAME 🚢 [調試版]", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家區域
            with Vertical():
                self.player_grid = DebugGameGrid(self.player_board, "🎮 你的戰場", clickable=True, show_ships=True)
                yield self.player_grid
            
            # 控制面板
            yield self.placement_panel
            
            # AI 區域  
            with Vertical():
                self.ai_grid = DebugGameGrid(self.ai_board, "🤖 敵方戰場", clickable=False, show_ships=False)
                yield self.ai_grid
    
    def on_mount(self):
        """應用啟動時的初始化"""
        print("🚀 調試版遊戲啟動")
        super().on_mount()
        
        # 延遲半秒後自動放置一些測試船隻
        self.set_timer(0.5, self.auto_place_test_ships)
    
    def auto_place_test_ships(self):
        """自動放置測試船隻"""
        print("\n🔧 自動放置測試船隻...")
        
        # 手動為玩家放置船隻
        test_ship = Ship("測試船", 2)
        if self.player_board.place_ship(test_ship, 1, 1, Orientation.HORIZONTAL):
            print("✅ 成功放置測試船在 (1,1)")
        else:
            print("❌ 無法放置測試船")
        
        print(f"📊 玩家棋盤狀態:")
        for row in range(3):
            line = ""
            for col in range(3):
                state = self.player_board.grid[row][col]
                line += f"{state.value} "
            print(f"  第{row}行: {line}")
        
        # 強制更新網格
        print("\n🔄 強制更新玩家網格...")
        if self.player_grid:
            self.player_grid.update_grid()
        else:
            print("❌ player_grid 為 None")
        
        print("\n🔄 強制更新AI網格...")
        if self.ai_grid:
            self.ai_grid.update_grid()
        else:
            print("❌ ai_grid 為 None")

def main():
    """運行調試版本"""
    print("🔍 啟動潛艇對決調試版本...")
    print("📝 這個版本會輸出詳細的調試信息")
    print("   包括網格更新、狀態變更等")
    print()
    
    app = DebugBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
