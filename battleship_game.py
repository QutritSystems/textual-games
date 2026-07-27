#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚢 潛艇對決 (Battleship Game)
==========================

一個使用 Textual 框架實現的終端戰艦遊戲。
玩家需要在 10x10 網格上放置船隻，然後與 AI 對手進行回合制戰鬥。

Features:
- 10x10 戰鬥網格
- 5種不同大小的船隻
- 智能 AI 對手
- 直觀的 UI 介面
- 回合制戰鬥系統
"""

from __future__ import annotations
import random
from enum import Enum
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass, field

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Label
from textual.reactive import reactive, Reactive
from textual import events
from textual.message import Message


class CellState(Enum):
    """網格單元狀態"""
    EMPTY = "~~~"      # 空白水域
    SHIP = "[S]"       # 船隻
    HIT = "<X>"        # 命中
    MISS = " o "       # 未命中
    SUNK = "XXX"       # 沉船


class GamePhase(Enum):
    """遊戲階段"""
    SETUP = "setup"           # 船隻放置階段
    BATTLE = "battle"         # 戰鬥階段
    GAME_OVER = "game_over"   # 遊戲結束


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
        """檢查船隻是否已沉沒"""
        return len(self.hits) >= self.size
    
    def hit(self, position: Tuple[int, int]) -> bool:
        """攻擊船隻的指定位置"""
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
        """檢查船隻放置位置是否有效"""
        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > self.size:
                return False
            positions = [(row, col + i) for i in range(ship_size)]
        else:  # VERTICAL
            if row + ship_size > self.size:
                return False
            positions = [(row + i, col) for i in range(ship_size)]
        
        # 檢查位置是否已被佔用（包括周圍一格的緩衝區）
        for pos_row, pos_col in positions:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    check_row, check_col = pos_row + dr, pos_col + dc
                    if (0 <= check_row < self.size and 0 <= check_col < self.size and
                        (check_row, check_col) in self.ship_positions):
                        return False
        
        return True
    
    def place_ship(self, ship: Ship, row: int, col: int, orientation: Orientation) -> bool:
        """在棋盤上放置船隻"""
        if not self.is_valid_position(row, col, ship.size, orientation):
            return False
        
        if orientation == Orientation.HORIZONTAL:
            positions = [(row, col + i) for i in range(ship.size)]
        else:  # VERTICAL
            positions = [(row + i, col) for i in range(ship.size)]
        
        ship.positions = positions
        self.ships.append(ship)
        for pos in positions:
            self.ship_positions.add(pos)
            self.grid[pos[0]][pos[1]] = CellState.SHIP
        
        return True
    
    def attack(self, row: int, col: int) -> CellState:
        """攻擊指定位置"""
        if self.grid[row][col] in [CellState.HIT, CellState.MISS, CellState.SUNK]:
            return self.grid[row][col]  # 已經攻擊過
        
        # 檢查是否命中船隻
        for ship in self.ships:
            if ship.hit((row, col)):
                self.grid[row][col] = CellState.HIT
                if ship.is_sunk:
                    # 標記整艘船為沉沒
                    for pos in ship.positions:
                        self.grid[pos[0]][pos[1]] = CellState.SUNK
                    return CellState.SUNK
                return CellState.HIT
        
        self.grid[row][col] = CellState.MISS
        return CellState.MISS
    
    def all_ships_sunk(self) -> bool:
        """檢查所有船隻是否都已沉沒"""
        return all(ship.is_sunk for ship in self.ships)


class GridCell(Static):
    """網格單元 Widget"""
    
    def __init__(self, row: int, col: int, state: CellState = CellState.EMPTY, clickable: bool = True):
        super().__init__()
        self.row = row
        self.col = col
        self.state = state
        self.clickable = clickable
        self.update_display()
    
    def update_display(self):
        """更新單元顯示"""
        self.update(self.state.value)
    
    def set_state(self, state: CellState):
        """設置單元狀態"""
        self.state = state
        self.update_display()
    
    class CellClicked(Message):
        """單元點擊事件"""
        def __init__(self, row: int, col: int) -> None:
            super().__init__()
            self.row = row
            self.col = col
    
    def on_click(self) -> None:
        """處理點擊事件"""
        if self.clickable:
            self.post_message(self.CellClicked(self.row, self.col))


class GameGrid(Container):
    """遊戲網格容器"""
    
    def __init__(self, board: GameBoard, title: str, clickable: bool = True, show_ships: bool = True):
        super().__init__()
        self.board = board
        self.title = title
        self.clickable = clickable
        self.show_ships = show_ships  # 是否顯示船隻位置
        self.cells: List[List[GridCell]] = []
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素"""
        with Vertical():
            yield Label(self.title)
            for row in range(self.board.size):
                cell_row = []
                with Horizontal():
                    for col in range(self.board.size):
                        # 初始化時使用空白狀態，稍後由 update_grid 更新
                        cell = GridCell(row, col, CellState.EMPTY, self.clickable)
                        cell_row.append(cell)
                        yield cell
                self.cells.append(cell_row)
    
    def on_mount(self) -> None:
        """組件掛載後初始化網格"""
        self.update_grid()
    
    def update_grid(self):
        """更新網格顯示"""
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell_state = self.board.grid[row][col]
                
                # 如果是 AI 戰場且不顯示船隻，則隱藏未被攻擊的船隻
                if not self.show_ships and cell_state == CellState.SHIP:
                    display_state = CellState.EMPTY
                else:
                    display_state = cell_state
                
                self.cells[row][col].set_state(display_state)


class ShipPlacementPanel(Container):
    """船隻放置面板"""
    
    def __init__(self):
        super().__init__()
        self.ships_to_place = [
            ("航空母艦", 5),
            ("戰艦", 4), 
            ("巡洋艦", 3),
            ("驅逐艦", 2),
            ("潛艇", 1)
        ]
        self.current_ship_index = 0
        self.current_orientation = Orientation.HORIZONTAL
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素"""
        with Vertical():
            yield Label("🚢 船隻放置階段", id="placement-title")
            yield Label("", id="current-ship")
            yield Label("", id="orientation")
            yield Button("切換方向 (R)", id="rotate-btn")
            yield Button("自動放置 (A)", id="auto-place-btn")
            yield Button("開始戰鬥", id="start-battle-btn", disabled=True)
    
    def on_mount(self) -> None:
        """組件掛載後初始化"""
        self.update_display()
    
    def update_display(self):
        """更新顯示信息"""
        if self.current_ship_index < len(self.ships_to_place):
            ship_name, ship_size = self.ships_to_place[self.current_ship_index]
            self.query_one("#current-ship").update(f"當前: {ship_name} ({ship_size}格)")
            self.query_one("#orientation").update(f"方向: {'水平' if self.current_orientation == Orientation.HORIZONTAL else '垂直'}")
        else:
            self.query_one("#current-ship").update("所有船隻已放置完成!")
            self.query_one("#start-battle-btn").disabled = False
    
    def get_current_ship(self) -> Optional[Tuple[str, int]]:
        """獲取當前要放置的船隻"""
        if self.current_ship_index < len(self.ships_to_place):
            return self.ships_to_place[self.current_ship_index]
        return None
    
    def next_ship(self):
        """移動到下一艘船"""
        self.current_ship_index += 1
        self.update_display()


class AIPlayer:
    """AI 對手"""
    
    def __init__(self, board: GameBoard):
        self.board = board
        self.target_queue: List[Tuple[int, int]] = []
        self.hit_positions: List[Tuple[int, int]] = []
        self.setup_ships()
    
    def setup_ships(self):
        """自動設置 AI 的船隻"""
        ships_data = [
            ("AI-航空母艦", 5),
            ("AI-戰艦", 4),
            ("AI-巡洋艦", 3),
            ("AI-驱逐舰", 2),
            ("AI-潛艇", 1)
        ]
        
        for ship_name, ship_size in ships_data:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                
                ship = Ship(ship_name, ship_size)
                if self.board.place_ship(ship, row, col, orientation):
                    placed = True
                attempts += 1
    
    def make_attack(self) -> Tuple[int, int]:
        """AI 進行攻擊"""
        # 如果有未完成的目標，優先攻擊
        if self.target_queue:
            return self.target_queue.pop(0)
        
        # 智能攻擊：如果有命中但未沉沒的船隻，攻擊周圍
        if self.hit_positions:
            last_hit = self.hit_positions[-1]
            adjacent_positions = self._get_adjacent_positions(last_hit)
            for pos in adjacent_positions:
                if self._is_valid_target(pos):
                    return pos
        
        # 隨機攻擊
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if self._is_valid_target((row, col)):
                return row, col
    
    def _get_adjacent_positions(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """獲取相鄰位置"""
        row, col = pos
        adjacent = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 10 and 0 <= new_col < 10:
                adjacent.append((new_row, new_col))
        return adjacent
    
    def _is_valid_target(self, pos: Tuple[int, int]) -> bool:
        """檢查位置是否為有效攻擊目標"""
        row, col = pos
        return True  # 由於我們無法直接訪問玩家棋盤，假設所有位置都可攻擊
    
    def process_attack_result(self, pos: Tuple[int, int], result: CellState):
        """處理攻擊結果"""
        if result == CellState.HIT:
            self.hit_positions.append(pos)
            # 添加相鄰位置到目標隊列
            adjacent = self._get_adjacent_positions(pos)
            for adj_pos in adjacent:
                if adj_pos not in self.target_queue:
                    self.target_queue.append(adj_pos)
        elif result == CellState.SUNK:
            # 清除相關的目標隊列
            self.hit_positions.clear()
            self.target_queue.clear()


class BattleshipGame(App):
    """潛艇對決主應用"""
    
    CSS = """
    Screen {
        background: #001122;
    }
    
    GridCell {
        width: 3;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: solid white;
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
    
    game_phase: Reactive[GamePhase] = reactive(GamePhase.SETUP)
    current_player: Reactive[str] = reactive("player")
    
    def __init__(self):
        super().__init__()
        self.player_board = GameBoard()
        self.ai_board = GameBoard()
        self.ai_player = AIPlayer(self.ai_board)
        self.placement_panel = ShipPlacementPanel()
        
        # UI 組件
        self.player_grid: Optional[GameGrid] = None
        self.ai_grid: Optional[GameGrid] = None
    
    def compose(self) -> ComposeResult:
        """組合 UI 元素"""
        yield Label("🚢 潛艇對決 BATTLESHIP GAME 🚢", id="game-title")
        yield Label("", id="game-status")
        
        with Horizontal():
            # 玩家區域
            with Vertical():
                self.player_grid = GameGrid(self.player_board, "🎮 你的戰場", clickable=True)
                yield self.player_grid
            
            # 控制面板
            yield self.placement_panel
            
            # AI 區域  
            with Vertical():
                self.ai_grid = GameGrid(self.ai_board, "🤖 敵方戰場", clickable=False, show_ships=False)
                yield self.ai_grid
    
    def on_mount(self):
        """應用啟動時的初始化"""
        self.update_status("放置你的船隻...")
    
    def update_status(self, message: str):
        """更新遊戲狀態顯示"""
        self.query_one("#game-status").update(message)
    
    async def on_grid_cell_cell_clicked(self, event: GridCell.CellClicked) -> None:
        """處理網格單元點擊"""
        if self.game_phase == GamePhase.SETUP:
            await self.handle_ship_placement(event.row, event.col)
        elif self.game_phase == GamePhase.BATTLE and self.current_player == "player":
            await self.handle_player_attack(event.row, event.col)
    
    async def handle_ship_placement(self, row: int, col: int):
        """處理船隻放置"""
        current_ship = self.placement_panel.get_current_ship()
        if not current_ship:
            return
        
        ship_name, ship_size = current_ship
        ship = Ship(ship_name, ship_size)
        
        if self.player_board.place_ship(ship, row, col, self.placement_panel.current_orientation):
            self.player_grid.update_grid()
            self.placement_panel.next_ship()
            self.update_status(f"已放置 {ship_name}")
        else:
            self.update_status("無效位置，請重新選擇")
    
    async def handle_player_attack(self, row: int, col: int):
        """處理玩家攻擊"""
        result = self.ai_board.attack(row, col)
        self.ai_grid.update_grid()
        
        if result == CellState.HIT:
            self.update_status("命中！")
        elif result == CellState.SUNK:
            self.update_status("擊沉敵艦！")
        elif result == CellState.MISS:
            self.update_status("未命中")
            self.current_player = "ai"
            await self.ai_turn()
        
        if self.ai_board.all_ships_sunk():
            await self.game_over("player")
    
    async def ai_turn(self):
        """AI 回合"""
        self.update_status("AI 攻擊中...")
        
        # 延遲一下讓玩家看到狀態
        import asyncio
        await asyncio.sleep(1)
        
        attack_pos = self.ai_player.make_attack()
        result = self.player_board.attack(attack_pos[0], attack_pos[1])
        self.ai_player.process_attack_result(attack_pos, result)
        
        self.player_grid.update_grid()
        
        if result == CellState.HIT:
            self.update_status("AI 命中了你的船隻！")
        elif result == CellState.SUNK:
            self.update_status("AI 擊沉了你的船隻！")
        elif result == CellState.MISS:
            self.update_status("AI 攻擊未命中")
        
        if self.player_board.all_ships_sunk():
            await self.game_over("ai")
        else:
            self.current_player = "player"
    
    async def game_over(self, winner: str):
        """遊戲結束"""
        self.game_phase = GamePhase.GAME_OVER
        if winner == "player":
            self.update_status("🎉 恭喜！你獲得了勝利！")
        else:
            self.update_status("💀 遊戲結束，AI 獲勝")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """處理按鈕點擊"""
        if event.button.id == "rotate-btn":
            self.placement_panel.current_orientation = (
                Orientation.VERTICAL if self.placement_panel.current_orientation == Orientation.HORIZONTAL 
                else Orientation.HORIZONTAL
            )
            self.placement_panel.update_display()
        
        elif event.button.id == "auto-place-btn":
            await self.auto_place_ships()
        
        elif event.button.id == "start-battle-btn":
            self.game_phase = GamePhase.BATTLE
            # 更新 AI 網格為可點擊
            for row in range(self.ai_grid.board.size):
                for col in range(self.ai_grid.board.size):
                    self.ai_grid.cells[row][col].clickable = True
            self.update_status("戰鬥開始！點擊敵方戰場進行攻擊")
    
    async def auto_place_ships(self):
        """自動放置剩餘船隻"""
        while self.placement_panel.current_ship_index < len(self.placement_panel.ships_to_place):
            ship_name, ship_size = self.placement_panel.ships_to_place[self.placement_panel.current_ship_index]
            ship = Ship(ship_name, ship_size)
            
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                
                if self.player_board.place_ship(ship, row, col, orientation):
                    placed = True
                    self.placement_panel.next_ship()
                attempts += 1
        
        self.player_grid.update_grid()
        self.update_status("所有船隻已自動放置完成")
    
    def on_key(self, event: events.Key) -> None:
        """處理鍵盤輸入"""
        if event.key == "r" and self.game_phase == GamePhase.SETUP:
            # 切換船隻方向
            self.placement_panel.current_orientation = (
                Orientation.VERTICAL if self.placement_panel.current_orientation == Orientation.HORIZONTAL 
                else Orientation.HORIZONTAL
            )
            self.placement_panel.update_display()
        
        elif event.key == "a" and self.game_phase == GamePhase.SETUP:
            # 自動放置
            self.run_worker(self.auto_place_ships())
        
        elif event.key == "q":
            # 退出遊戲
            self.exit()


def main():
    """主函數"""
    app = BattleshipGame()
    app.run()


if __name__ == "__main__":
    main()
