#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復版潛艇對決 - 解決視覺效果問題
重新設計 GridCell 更新機制
"""

from battleship_game import *

class FixedGridCell(Static):
    """修復版網格單元"""
    
    def __init__(self, row: int, col: int, state: CellState = CellState.EMPTY, clickable: bool = True):
        # 直接使用狀態值作為初始內容
        super().__init__(state.value)
        self.row = row
        self.col = col
        self.state = state
        self.clickable = clickable
        print(f"🔧 創建 FixedGridCell ({row},{col}) 初始狀態: {state.name} = '{state.value}'")
    
    def set_state(self, state: CellState):
        """設置單元狀態 - 強制更新"""
        print(f"🔄 FixedGridCell ({self.row},{self.col}) 狀態更新: {self.state.name} -> {state.name} ('{state.value}')")
        self.state = state
        
        # 使用多種方法確保更新
        self.update(state.value)
        self.renderable = state.value
        
        # 強制重新渲染
        self.refresh()
        
        print(f"✅ FixedGridCell ({self.row},{self.col}) 更新完成，當前內容: '{self.renderable}'")
    
    class CellClicked(Message):
        """單元點擊事件"""
        def __init__(self, row: int, col: int) -> None:
            super().__init__()
            self.row = row
            self.col = col
    
    def on_click(self) -> None:
        """處理點擊事件"""
        if self.clickable:
            print(f"👆 點擊 FixedGridCell ({self.row},{self.col})")
            self.post_message(self.CellClicked(self.row, self.col))

class FixedGameGrid(GameGrid):
    """修復版遊戲網格"""
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素 - 使用修復版 GridCell"""
        print(f"🏗️  構建 FixedGameGrid: {self.title}")
        with Vertical():
            yield Label(self.title)
            for row in range(self.board.size):
                cell_row = []
                with Horizontal():
                    for col in range(self.board.size):
                        # 使用修復版 GridCell
                        cell = FixedGridCell(row, col, CellState.EMPTY, self.clickable)
                        cell_row.append(cell)
                        yield cell
                self.cells.append(cell_row)
        print(f"✅ FixedGameGrid 構建完成，網格大小: {len(self.cells)}x{len(self.cells[0])}")
    
    def update_grid(self):
        """更新網格顯示 - 增強調試"""
        print(f"🔄 更新 FixedGameGrid: {self.title}")
        print(f"   網格大小: {len(self.cells)}x{len(self.cells[0] if self.cells else [])}")
        print(f"   顯示船隻: {self.show_ships}")
        
        updated_count = 0
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell_state = self.board.grid[row][col]
                
                # AI 戰場隱藏船隻邏輯
                if not self.show_ships and cell_state == CellState.SHIP:
                    display_state = CellState.EMPTY
                else:
                    display_state = cell_state
                
                # 更新單元格
                if row < len(self.cells) and col < len(self.cells[row]):
                    old_state = self.cells[row][col].state
                    if old_state != display_state:
                        self.cells[row][col].set_state(display_state)
                        updated_count += 1
                        
                        # 調試前5x5區域
                        if row < 5 and col < 5:
                            print(f"   更新 ({row},{col}): {old_state.name} -> {display_state.name}")
        
        print(f"✅ FixedGameGrid 更新完成，共更新 {updated_count} 個格子")

class FixedBattleshipGame(BattleshipGame):
    """修復版潛艇對決遊戲"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    FixedGridCell {
        width: 4;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: solid white;
        color: white;
        background: #003366;
    }
    
    FixedGridCell:hover {
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
        """組合 UI 元素 - 使用修復版網格"""
        print("🚀 啟動 FixedBattleshipGame")
        yield Label("*** 潛艇對決 BATTLESHIP GAME *** [修復版]", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家區域
            with Vertical():
                print("🏗️  創建玩家網格...")
                self.player_grid = FixedGameGrid(self.player_board, "*** 你的戰場 ***", clickable=True, show_ships=True)
                yield self.player_grid
            
            # 控制面板
            yield self.placement_panel
            
            # AI 區域  
            with Vertical():
                print("🏗️  創建 AI 網格...")
                self.ai_grid = FixedGameGrid(self.ai_board, "*** 敵方戰場 ***", clickable=False, show_ships=False)
                yield self.ai_grid
        
        print("✅ FixedBattleshipGame UI 構建完成")
    
    def on_mount(self):
        """應用啟動時的初始化"""
        print("📱 FixedBattleshipGame.on_mount() 被調用")
        super().on_mount()
        
        # 立即放置測試船隻
        self.set_timer(1.0, self.place_test_ship)
    
    def place_test_ship(self):
        """放置測試船隻"""
        print("\n🚢 === 開始放置測試船隻 ===")
        
        # 為玩家放置測試船隻
        test_ship = Ship("測試船", 3)
        success = self.player_board.place_ship(test_ship, 2, 2, Orientation.HORIZONTAL)
        
        print(f"📊 船隻放置結果: {success}")
        if success:
            print(f"🎯 船隻位置: {test_ship.positions}")
            
            # 顯示棋盤狀態
            print("📋 玩家棋盤前5行:")
            for row in range(5):
                line = ""
                for col in range(5):
                    state = self.player_board.grid[row][col]
                    line += f"{state.value} "
                print(f"  第{row}行: {line}")
            
            # 強制更新玩家網格
            print("\n🔄 === 強制更新玩家網格 ===")
            if self.player_grid:
                self.player_grid.update_grid()
            else:
                print("❌ player_grid 為 None!")
        
        # 也更新 AI 網格
        print("\n🔄 === 更新 AI 網格 ===")
        if self.ai_grid:
            self.ai_grid.update_grid()
        else:
            print("❌ ai_grid 為 None!")
        
        self.update_status("🔧 測試船隻已放置！符號說明: ~~~ 水域, [S] 船隻, <X> 命中, o 未命中, XXX 沉船")
        print("✅ === 測試船隻放置完成 ===\n")
    
    async def on_fixed_grid_cell_cell_clicked(self, event: FixedGridCell.CellClicked) -> None:
        """處理修復版網格單元點擊"""
        print(f"🎯 收到點擊事件: ({event.row}, {event.col})")
        return await self.on_grid_cell_cell_clicked(event)

def main():
    """運行修復版本"""
    print("🔍 啟動潛艇對決修復版本...")
    print("這個版本會輸出詳細的調試信息")
    print("並強制更新網格顯示")
    print()
    
    app = FixedBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
