#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終修復版潛艇對決
解決所有已知的視覺效果問題
"""

from __future__ import annotations
import random
import asyncio
from enum import Enum
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass, field

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Label
from textual.reactive import reactive
from textual import events
from textual.message import Message

# 使用單字符符號確保顯示
class CellState(Enum):
    """網格單元狀態"""
    EMPTY = "~"      # 空白水域
    SHIP = "S"       # 船隻
    HIT = "X"        # 命中
    MISS = "o"       # 未命中
    SUNK = "#"       # 沉船

class GamePhase(Enum):
    """遊戲階段"""
    SETUP = "setup"
    BATTLE = "battle" 
    GAME_OVER = "game_over"

class Orientation(Enum):
    """船隻方向"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

@dataclass
class Ship:
    """船隻類別"""
    name: str
    size: int
    positions: List[Tuple[int, int]] = field(default_factory=list)
    hits: Set[Tuple[int, int]] = field(default_factory=set)
    
    @property
    def is_sunk(self) -> bool:
        return len(self.hits) >= self.size
    
    def hit(self, position: Tuple[int, int]) -> bool:
        if position in self.positions:
            self.hits.add(position)
            return True
        return False

class GameBoard:
    """遊戲棋盤"""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.ship_positions: Set[Tuple[int, int]] = set()
    
    def is_valid_position(self, row: int, col: int, ship_size: int, orientation: Orientation) -> bool:
        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > self.size:
                return False
            positions = [(row, col + i) for i in range(ship_size)]
        else:
            if row + ship_size > self.size:
                return False
            positions = [(row + i, col) for i in range(ship_size)]
        
        for pos_row, pos_col in positions:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    check_row, check_col = pos_row + dr, pos_col + dc
                    if (0 <= check_row < self.size and 0 <= check_col < self.size and
                        (check_row, check_col) in self.ship_positions):
                        return False
        return True
    
    def place_ship(self, ship: Ship, row: int, col: int, orientation: Orientation) -> bool:
        if not self.is_valid_position(row, col, ship.size, orientation):
            return False
        
        if orientation == Orientation.HORIZONTAL:
            positions = [(row, col + i) for i in range(ship.size)]
        else:
            positions = [(row + i, col) for i in range(ship.size)]
        
        ship.positions = positions
        self.ships.append(ship)
        for pos in positions:
            self.ship_positions.add(pos)
            self.grid[pos[0]][pos[1]] = CellState.SHIP
        
        return True
    
    def attack(self, row: int, col: int) -> CellState:
        if self.grid[row][col] in [CellState.HIT, CellState.MISS, CellState.SUNK]:
            return self.grid[row][col]
        
        for ship in self.ships:
            if ship.hit((row, col)):
                self.grid[row][col] = CellState.HIT
                if ship.is_sunk:
                    for pos in ship.positions:
                        self.grid[pos[0]][pos[1]] = CellState.SUNK
                    return CellState.SUNK
                return CellState.HIT
        
        self.grid[row][col] = CellState.MISS
        return CellState.MISS
    
    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk for ship in self.ships)

class FinalGridCell(Static):
    """最終版網格單元 - 確保視覺更新"""
    
    def __init__(self, row: int, col: int, clickable: bool = True):
        super().__init__("~")  # 初始化為水域
        self.row = row
        self.col = col
        self.clickable = clickable
        self.cell_state = CellState.EMPTY
    
    def set_display(self, state: CellState):
        """直接設置顯示內容"""
        self.cell_state = state
        self.update(state.value)
        
        # 根據狀態設置顏色
        if state == CellState.SHIP:
            self.styles.color = "green"
        elif state == CellState.HIT:
            self.styles.color = "red"
        elif state == CellState.SUNK:
            self.styles.color = "yellow"
        elif state == CellState.MISS:
            self.styles.color = "cyan"
        else:
            self.styles.color = "white"
    
    class CellClicked(Message):
        def __init__(self, row: int, col: int) -> None:
            super().__init__()
            self.row = row
            self.col = col
    
    def on_click(self) -> None:
        if self.clickable:
            self.post_message(self.CellClicked(self.row, self.col))

class FinalGameGrid(Container):
    """最終版遊戲網格"""
    
    def __init__(self, board: GameBoard, title: str, clickable: bool = True, show_ships: bool = True):
        super().__init__()
        self.board = board
        self.title = title
        self.clickable = clickable
        self.show_ships = show_ships
        self.cells: List[List[FinalGridCell]] = []
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.title)
            with Container(id="grid-container"):
                for row in range(self.board.size):
                    cell_row = []
                    with Horizontal():
                        for col in range(self.board.size):
                            cell = FinalGridCell(row, col, self.clickable)
                            cell_row.append(cell)
                            yield cell
                    self.cells.append(cell_row)
    
    def on_mount(self) -> None:
        """掛載後立即更新顯示"""
        self.call_later(self.force_update)
    
    def force_update(self):
        """強制更新所有格子"""
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell_state = self.board.grid[row][col]
                
                # AI 戰場隱藏船隻
                if not self.show_ships and cell_state == CellState.SHIP:
                    display_state = CellState.EMPTY
                else:
                    display_state = cell_state
                
                self.cells[row][col].set_display(display_state)

class FinalBattleshipGame(App):
    """最終版潛艇對決遊戲"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    FinalGridCell {
        width: 3;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: none;
        background: #003366;
    }
    
    FinalGridCell:hover {
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
    
    game_phase: reactive = reactive(GamePhase.SETUP)
    
    def __init__(self):
        super().__init__()
        self.player_board = GameBoard()
        self.ai_board = GameBoard()
        self.setup_ai()
        self.player_grid = None
        self.ai_grid = None
        self.ships_to_place = [("航母", 5), ("戰艦", 4), ("巡洋", 3), ("驅逐", 2), ("潛艇", 1)]
        self.current_ship_index = 0
        self.current_orientation = Orientation.HORIZONTAL
        self.current_player = "player"
    
    def setup_ai(self):
        """設置 AI 船隻"""
        ships_data = [("AI航母", 5), ("AI戰艦", 4), ("AI巡洋", 3), ("AI驅逐", 2), ("AI潛艇", 1)]
        
        for ship_name, ship_size in ships_data:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                ship = Ship(ship_name, ship_size)
                if self.ai_board.place_ship(ship, row, col, orientation):
                    placed = True
                attempts += 1
    
    def compose(self) -> ComposeResult:
        yield Label("*** 潛艇對決 *** [最終修復版]", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家戰場
            with Vertical():
                self.player_grid = FinalGameGrid(self.player_board, "你的戰場", True, True)
                yield self.player_grid
            
            # 控制面板
            with Vertical():
                yield Label("控制面板", id="panel-title")
                yield Label("", id="current-ship")
                yield Button("切換方向", id="rotate")
                yield Button("自動放置", id="auto-place")
                yield Button("開始戰鬥", id="start-battle", disabled=True)
                yield Label("", id="legend")
            
            # AI 戰場
            with Vertical():
                self.ai_grid = FinalGameGrid(self.ai_board, "敵方戰場", False, False)
                yield self.ai_grid
    
    def on_mount(self):
        """初始化"""
        self.update_status("點擊你的戰場放置船隻")
        self.update_ship_info()
        self.query_one("#legend").update("符號: ~ 水域, S 船隻, X 命中, o 未命中, # 沉船")
        
        # 自動放置測試船隻（僅用於演示）
        self.set_timer(1.0, self.demo_place_ship)
    
    def demo_place_ship(self):
        """演示自動放置一艘船"""
        if self.current_ship_index < len(self.ships_to_place):
            ship_name, ship_size = self.ships_to_place[self.current_ship_index]
            ship = Ship(ship_name, ship_size)
            if self.player_board.place_ship(ship, 1, 1, Orientation.HORIZONTAL):
                self.player_grid.force_update()
                self.current_ship_index += 1
                self.update_ship_info()
                self.update_status(f"已放置 {ship_name} (演示)")
    
    def update_status(self, message: str):
        self.query_one("#game-status").update(message)
    
    def update_ship_info(self):
        if self.current_ship_index < len(self.ships_to_place):
            ship_name, ship_size = self.ships_to_place[self.current_ship_index]
            self.query_one("#current-ship").update(f"當前: {ship_name} ({ship_size}格)")
        else:
            self.query_one("#current-ship").update("所有船隻已放置")
            self.query_one("#start-battle").disabled = False
    
    async def on_final_grid_cell_cell_clicked(self, event: FinalGridCell.CellClicked) -> None:
        """處理格子點擊"""
        if self.game_phase == GamePhase.SETUP:
            await self.handle_ship_placement(event.row, event.col)
        elif self.game_phase == GamePhase.BATTLE and self.current_player == "player":
            await self.handle_attack(event.row, event.col)
    
    async def handle_ship_placement(self, row: int, col: int):
        """處理船隻放置"""
        if self.current_ship_index >= len(self.ships_to_place):
            return
        
        ship_name, ship_size = self.ships_to_place[self.current_ship_index]
        ship = Ship(ship_name, ship_size)
        
        if self.player_board.place_ship(ship, row, col, self.current_orientation):
            self.player_grid.force_update()
            self.current_ship_index += 1
            self.update_ship_info()
            self.update_status(f"已放置 {ship_name}")
        else:
            self.update_status("無效位置，請重新選擇")
    
    async def handle_attack(self, row: int, col: int):
        """處理攻擊"""
        result = self.ai_board.attack(row, col)
        self.ai_grid.force_update()
        
        if result == CellState.HIT:
            self.update_status("命中！")
        elif result == CellState.SUNK:
            self.update_status("擊沉敵艦！")
        elif result == CellState.MISS:
            self.update_status("未命中")
            await self.ai_attack()
        
        if self.ai_board.all_ships_sunk():
            self.update_status("🎉 你獲勝了！")
    
    async def ai_attack(self):
        """AI 攻擊"""
        self.update_status("AI 攻擊中...")
        await asyncio.sleep(1)
        
        # 隨機攻擊
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if self.player_board.grid[row][col] in [CellState.EMPTY, CellState.SHIP]:
                break
        
        result = self.player_board.attack(row, col)
        self.player_grid.force_update()
        
        if result == CellState.HIT:
            self.update_status("AI 命中了你的船！")
        elif result == CellState.SUNK:
            self.update_status("AI 擊沉了你的船！")
        elif result == CellState.MISS:
            self.update_status("AI 攻擊未命中，輪到你了")
        
        if self.player_board.all_ships_sunk():
            self.update_status("💀 AI 獲勝了！")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "rotate":
            self.current_orientation = (Orientation.VERTICAL if self.current_orientation == Orientation.HORIZONTAL 
                                     else Orientation.HORIZONTAL)
            self.update_status(f"方向: {'垂直' if self.current_orientation == Orientation.VERTICAL else '水平'}")
        
        elif event.button.id == "auto-place":
            await self.auto_place_all()
        
        elif event.button.id == "start-battle":
            self.game_phase = GamePhase.BATTLE
            self.ai_grid.clickable = True
            for row in self.ai_grid.cells:
                for cell in row:
                    cell.clickable = True
            self.update_status("戰鬥開始！點擊敵方戰場攻擊")
    
    async def auto_place_all(self):
        """自動放置所有剩餘船隻"""
        while self.current_ship_index < len(self.ships_to_place):
            ship_name, ship_size = self.ships_to_place[self.current_ship_index]
            ship = Ship(ship_name, ship_size)
            
            placed = False
            for _ in range(100):  # 最多嘗試100次
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                
                if self.player_board.place_ship(ship, row, col, orientation):
                    placed = True
                    break
            
            if placed:
                self.current_ship_index += 1
            else:
                break
        
        self.player_grid.force_update()
        self.update_ship_info()
        self.update_status("自動放置完成")
    
    def on_key(self, event: events.Key) -> None:
        if event.key == "q":
            self.exit()

def main():
    app = FinalBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
