#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Battleship AI Arena
A sandbox for testing and hot-swapping AI targeting algorithms.
"""
import asyncio
import importlib
import random
import hashlib
from pathlib import Path
from typing import List, Tuple

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Label, RichLog
from textual.message import Message
from textual import work
from textual.css.query import NoMatches

from battleship_core import GameBoard, CellState, GamePhase, GameMode, Orientation, Ship
import battleship_strategies


class StrategyLoader:
    """Load a changed strategy without mutating the currently active module."""

    def __init__(self, path: Path):
        self.path = path
        self._module = battleship_strategies
        self._fingerprint = self._fingerprint_file()

    def _fingerprint_file(self) -> str | None:
        try:
            return hashlib.sha256(self.path.read_bytes()).hexdigest()
        except OSError:
            return None

    def load(self):
        fingerprint = self._fingerprint_file()
        if fingerprint is None:
            print("Strategy file is temporarily unreadable.")
            return self._module
            
        if fingerprint == self._fingerprint:
            return self._module

        try:
            module_name = f"_battleship_strategy_{fingerprint}"
            spec = importlib.util.spec_from_file_location(module_name, self.path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Unable to load strategy from {self.path}")

            candidate = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(candidate)
            if not (callable(getattr(candidate, "decide_attack_p1", None)) and 
                    callable(getattr(candidate, "decide_attack_p2", None))):
                raise TypeError("Strategy module must define decide_attack_p1 and decide_attack_p2")

            self._module = candidate
            self._fingerprint = fingerprint
        except Exception as e:
            # On error, we retain the old module but print the error so the user can fix it.
            print(f"Error loading strategy: {e}")
            
        return self._module


class GridCell(Static):
    """Arena Grid Cell"""
    
    def __init__(self, row: int, col: int, clickable: bool = True):
        super().__init__("~")
        self.row = row
        self.col = col
        self.clickable = clickable
        self.cell_state = CellState.EMPTY
    
    def set_display(self, state: CellState):
        self.cell_state = state
        self.update(state.value)
        
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
        def __init__(self, row: int, col: int, cell: "GridCell | None" = None) -> None:
            super().__init__()
            self.row = row
            self.col = col
            self.cell = cell

        @property
        def control(self) -> "GridCell | None":
            return self.cell
            
    def on_click(self) -> None:
        if self.clickable:
            self.post_message(self.CellClicked(self.row, self.col, self))

class GameGrid(Container):
    """Arena Game Grid"""
    
    def __init__(self, board: GameBoard, title: str, clickable: bool = True, show_ships: bool = True):
        super().__init__()
        self.board = board
        self.title = title
        self.clickable = clickable
        self.show_ships = show_ships
        self.cells: List[List[GridCell]] = []
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.title)
            with Container(id="grid-container"):
                for row in range(self.board.size):
                    cell_row = []
                    with Horizontal():
                        for col in range(self.board.size):
                            cell = GridCell(row, col, self.clickable)
                            cell_row.append(cell)
                            yield cell
                    self.cells.append(cell_row)
                    
    def on_mount(self) -> None:
        self.call_later(self.force_update)
        
    def force_update(self):
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell_state = self.board.grid[row][col]
                
                if not self.show_ships and cell_state == CellState.SHIP:
                    display_state = CellState.EMPTY
                else:
                    display_state = cell_state
                    
                self.cells[row][col].set_display(display_state)

class BattleshipArena(App):
    """The AI Arena Application"""
    
    CSS = """
    Screen {
        background: #001122;
        align: center middle;
    }
    
    #game-title {
        text-align: center;
        text-style: bold;
        color: yellow;
        margin-bottom: 1;
    }
    
    #status-bar {
        background: #003366;
        color: white;
        text-align: center;
        padding: 1;
        margin-bottom: 1;
        border: solid white;
    }
    
    GridCell {
        width: 2;
        height: 1;
        margin: 0;
        padding: 0;
        text-align: center;
        border: none;
        background: #002244;
    }
    
    GridCell:hover {
        background: #006699;
    }
    
    #grid-container {
        border: solid white;
        padding: 0;
        margin: 0;
        width: 22;
        height: 12;
    }

    #arena-row {
        width: 100%;
        height: auto;
        overflow-x: auto;
    }
    
    Horizontal {
        height: 1;
        margin: 0;
        padding: 0;
    }
    
    .panel {
        border: solid cyan;
        padding: 1;
        margin: 1;
        width: 25;
    }
    
    #log-title {
        color: magenta;
        text-style: bold;
        margin-top: 1;
        margin-left: 2;
    }
    
    #thinking-log {
        background: #000c1a;
        color: #cccccc;
        border: solid magenta;
        margin: 0 2;
        height: 10;
        min-height: 5;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.player_board = GameBoard(10)
        self.ai_board = GameBoard(10)
        self.game_phase = GamePhase.SETUP
        self.game_mode = GameMode.MANUAL
        self.ai_turn_in_progress = False
        self.auto_battle_running = False
        self.auto_battle_worker = None
        self.auto_battle_generation = 0
        self.strategy_loader = StrategyLoader(Path(battleship_strategies.__file__).resolve())
        
        self.ships_to_place = [
            ("航空母艦", 5),
            ("戰艦", 4),
            ("巡洋艦", 3),
            ("潛艇", 3),
            ("驅逐艦", 2)
        ]
        
    def compose(self) -> ComposeResult:
        yield Label("⚔️ Battleship AI Arena ⚔️", id="game-title")
        yield Label("歡迎來到 AI 競技場！", id="status-bar")
        
        with Horizontal(id="arena-row"):
            with Vertical():
                self.player_grid = GameGrid(self.player_board, "你的戰場 (Player)", True, True)
                yield self.player_grid
                
            with Vertical(classes="panel"):
                yield Label("控制台")
                yield Button("自動佈陣", id="auto-place")
                yield Button("開始手動戰鬥", id="start-battle", disabled=True)
                yield Label("---")
                yield Button("AI vs AI 對戰", id="start-ai-battle")
                yield Button("停止對戰", id="stop-battle", disabled=True)
                yield Label(" ")
                yield Label("💡 Live Hack: 戰鬥中修改\nbattleship_strategies.py\n可即時改變 AI 攻擊邏輯！")
                
            with Vertical():
                self.ai_grid = GameGrid(self.ai_board, "沙盒戰場 (AI)", False, False)
                yield self.ai_grid
                
        yield Label("🧠 AI 思考與戰況轉播面板：", id="log-title")
        yield RichLog(id="thinking-log", max_lines=100, markup=True)
                
    def update_status(self, message: str):
        if not self.is_running or not self.is_mounted:
            return
        try:
            self.query_one("#status-bar").update(message)
        except NoMatches:
            pass
        
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "auto-place":
            self.auto_place_ships(self.player_board)
            self.player_grid.force_update()
            
            # Setup AI ships too
            self.auto_place_ships(self.ai_board)
            self.ai_grid.force_update()
            
            self.update_status("雙方佈陣完成，可以開始戰鬥！")
            self.query_one("#start-battle").disabled = False
            self.query_one("#auto-place").disabled = True
            
        elif event.button.id == "start-battle":
            self.game_phase = GamePhase.BATTLE
            self.game_mode = GameMode.MANUAL
            self.ai_grid.clickable = True
            for row in self.ai_grid.cells:
                for cell in row:
                    cell.clickable = True
            self.query_one("#start-battle").disabled = True
            self.query_one("#start-ai-battle").disabled = True
            self.update_status("戰鬥開始！點擊右方沙盒戰場進行攻擊。")
            
        elif event.button.id == "start-ai-battle":
            if self.auto_battle_running:
                return
                
            # State Reset for AI vs AI
            self.auto_place_ships(self.player_board)
            self.player_grid.force_update()
            self.auto_place_ships(self.ai_board)
            self.ai_grid.force_update()
            
            self.game_phase = GamePhase.BATTLE
            self.game_mode = GameMode.AI_VS_AI
            
            # Disable manual interactions
            self.player_grid.clickable = False
            self.ai_grid.clickable = False
            for row in self.player_grid.cells:
                for cell in row:
                    cell.clickable = False
            for row in self.ai_grid.cells:
                for cell in row:
                    cell.clickable = False
                    
            # Toggle buttons
            self.query_one("#auto-place").disabled = True
            self.query_one("#start-battle").disabled = True
            self.query_one("#start-ai-battle").disabled = True
            self.query_one("#stop-battle").disabled = False
            
            self.update_status("🤖 AI vs AI 自動戰鬥開始！")
            
            # Start Auto Battle Worker
            self.auto_battle_running = True
            self.auto_battle_generation += 1
            self.auto_battle_worker = self.run_auto_battle(self.auto_battle_generation)
            
        elif event.button.id == "stop-battle":
            self.auto_battle_running = False
            if self.auto_battle_worker:
                self.auto_battle_worker.cancel()
                await self.auto_battle_worker.wait()
                self.auto_battle_worker = None
                
            self.game_phase = GamePhase.GAME_OVER
            self.game_mode = GameMode.MANUAL
            
            # Crucial: Re-enable UI so it actually acts like manual mode again
            self.player_grid.clickable = True
            self.ai_grid.clickable = True
            for row in self.player_grid.cells:
                for cell in row:
                    cell.clickable = True
            for row in self.ai_grid.cells:
                for cell in row:
                    cell.clickable = True
                    
            self.update_status("戰鬥已中止。")
            self.query_one("#stop-battle").disabled = True
            self.query_one("#start-ai-battle").disabled = False
            self.query_one("#auto-place").disabled = False
            
    def auto_place_ships(self, board: GameBoard):
        board.ships = []
        board.ship_positions.clear()
        board.grid = [[CellState.EMPTY for _ in range(board.size)] for _ in range(board.size)]
        
        for name, size in self.ships_to_place:
            placed = False
            while not placed:
                r = random.randrange(board.size)
                c = random.randrange(board.size)
                ori = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                placed = board.place_ship(Ship(name, size), r, c, ori)

    async def on_grid_cell_cell_clicked(self, event: GridCell.CellClicked) -> None:
        if self.game_phase != GamePhase.BATTLE or self.ai_turn_in_progress:
            return
            
        # Ensure it's the AI grid being clicked
        cell_clicked = event.control
        is_ai_grid = False
        for row in self.ai_grid.cells:
            if cell_clicked in row:
                is_ai_grid = True
                break
                
        if not is_ai_grid:
            return
            
        # Player Attack
        try:
            result = self.ai_board.attack(event.row, event.col)
            self.ai_grid.force_update()
            
            if result == CellState.HIT:
                self.update_status("你命中了敵艦！")
            elif result == CellState.SUNK:
                self.update_status("你擊沉了敵艦！")
            elif result == CellState.MISS:
                self.update_status("你未命中。")
            
            if self.ai_board.all_ships_sunk():
                self.game_phase = GamePhase.GAME_OVER
                self.update_status("🎉 你獲勝了！")
                return
                
            # Trigger AI Turn
            if result == CellState.MISS:
                self.ai_turn_in_progress = True
                self.set_ai_cells_clickable(False)
                self.run_ai_turn()
        except ValueError:
             # Already attacked
             pass
             
    @work(group="auto_battle", exclusive=True)
    async def run_auto_battle(self, generation: int):
        try:
            current_player = "p1"
            while self.auto_battle_running and self.game_phase == GamePhase.BATTLE:
                self.update_status(f"AI ({current_player.upper()}) 思考中 (Hot-reloading strategy...)")
                await asyncio.sleep(0.3)
                
                if not self.auto_battle_running:
                    break

                strategy_module = self.strategy_loader.load()
                
                if current_player == "p1":
                    # P1 attacks AI board
                    grid_snapshot = tuple(tuple(CellState.EMPTY if cell == CellState.SHIP else cell for cell in row) for row in self.ai_board.grid)
                    decision = strategy_module.decide_attack_p1(grid_snapshot)
                    board_to_attack = self.ai_board
                    grid_to_update = self.ai_grid
                    next_player = "p2"
                    opp_name = "Player 2"
                else:
                    # P2 attacks Player board
                    grid_snapshot = tuple(tuple(CellState.EMPTY if cell == CellState.SHIP else cell for cell in row) for row in self.player_board.grid)
                    decision = strategy_module.decide_attack_p2(grid_snapshot)
                    board_to_attack = self.player_board
                    grid_to_update = self.player_grid
                    next_player = "p1"
                    opp_name = "Player 1"

                try:
                    (row, col), reason = self.parse_decision(decision)
                    # Write to RichLog
                    player_label = "[bold green]AI Player 1 (Left)[/bold green]" if current_player == "p1" else "[bold cyan]AI Player 2 (Right)[/bold cyan]"
                    try:
                        self.query_one("#thinking-log").write(f"{player_label}: {reason}")
                    except NoMatches:
                        pass
                except ValueError as e:
                    raise ValueError(f"Strategy for {current_player} error: {e}")
                if not (0 <= row < board_to_attack.size and 0 <= col < board_to_attack.size):
                    raise ValueError(f"Strategy for {current_player} returned out-of-bounds position: ({row}, {col})")
                
                if board_to_attack.grid[row][col] in {CellState.HIT, CellState.MISS, CellState.SUNK}:
                    raise ValueError(f"Strategy for {current_player} selected an already attacked position: ({row}, {col})")
                
                result = board_to_attack.attack(row, col)
                grid_to_update.force_update()

                if result == CellState.HIT:
                    self.update_status(f"{current_player.upper()} 命中 ({row}, {col})！")
                elif result == CellState.SUNK:
                    self.update_status(f"{current_player.upper()} 擊沉了 {opp_name} 的船！ ({row}, {col})")
                elif result == CellState.MISS:
                    self.update_status(f"{current_player.upper()} 攻擊 ({row}, {col}) 未命中。")

                if board_to_attack.all_ships_sunk():
                    self.game_phase = GamePhase.GAME_OVER
                    self.auto_battle_running = False
                    self.update_status(f"🎉 {current_player.upper()} 獲勝了！")
                    
                    self.query_one("#stop-battle").disabled = True
                    self.query_one("#start-ai-battle").disabled = False
                    self.query_one("#auto-place").disabled = False
                    break
                
                current_player = next_player
                await asyncio.sleep(0.3)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.update_status(f"⚠️ AI 策略錯誤: {e}")
            if self.auto_battle_generation == generation:
                self.auto_battle_running = False
                self.game_phase = GamePhase.GAME_OVER
                self.query_one("#stop-battle").disabled = True
                self.query_one("#start-ai-battle").disabled = False
                self.query_one("#auto-place").disabled = False
        finally:
            if self.auto_battle_generation == generation:
                self.auto_battle_running = False

    async def on_unmount(self) -> None:
        if self.auto_battle_worker:
            self.auto_battle_worker.cancel()
            await self.auto_battle_worker.wait()

    def set_ai_cells_clickable(self, clickable: bool) -> None:
        self.ai_grid.clickable = clickable
        for row in self.ai_grid.cells:
            for cell in row:
                cell.clickable = clickable

    def parse_decision(self, decision) -> Tuple[Tuple[int, int], str]:
        """Safely parse decision to (row, col) and reasoning, supporting both legacy and new signatures."""
        if not isinstance(decision, (tuple, list)) or len(decision) != 2:
            raise ValueError("Strategy decision must be a tuple/list of length 2")
            
        # Case 1: ((row, col), reason)
        if isinstance(decision[0], (tuple, list)):
            coords = decision[0]
            if len(coords) != 2 or type(coords[0]) is not int or type(coords[1]) is not int:
                raise ValueError("Coordinates must be a pair of integers")
            reason = str(decision[1])
            return (coords[0], coords[1]), reason
            
        # Case 2: (row, col)
        if type(decision[0]) is int and type(decision[1]) is int:
            return (decision[0], decision[1]), "執行標準探測"
            
        raise ValueError("Unknown decision format. Must be (row, col) or ((row, col), reason)")

    @work(exclusive=True)
    async def run_ai_turn(self):
        self.update_status("AI 思考中 (Hot-reloading strategy...)")
        await asyncio.sleep(0.5) # Simulate thinking and visual pacing
        
        try:
            # Load a changed strategy only after its replacement module is valid.
            strategy_module = self.strategy_loader.load()
            grid_snapshot = tuple(tuple(row) for row in self.player_board.grid)
            decision = strategy_module.decide_attack(grid_snapshot)
            
            (row, col), reason = self.parse_decision(decision)
            
            # Stream thoughts to RichLog
            try:
                self.query_one("#thinking-log").write(f"[bold red]AI (Enemy)[/bold red]: {reason}")
            except NoMatches:
                pass
            if not (0 <= row < self.player_board.size and 0 <= col < self.player_board.size):
                raise ValueError(f"Strategy returned out-of-bounds position: ({row}, {col})")
            if self.player_board.grid[row][col] in {
                CellState.HIT,
                CellState.MISS,
                CellState.SUNK,
            }:
                raise ValueError(f"Strategy selected an already attacked position: ({row}, {col})")
            
            result = self.player_board.attack(row, col)
            self.player_grid.force_update()
            
            if result == CellState.HIT:
                self.update_status(f"AI 命中 ({row}, {col})！")
                # AI gets another turn on hit? Let's just make it strictly alternating for simpler testing right now.
                # Actually, standard battleship means alternating turns usually, let's keep it alternating.
            elif result == CellState.SUNK:
                self.update_status(f"AI 擊沉了你的船！ ({row}, {col})")
            elif result == CellState.MISS:
                self.update_status(f"AI 攻擊 ({row}, {col}) 未命中。輪到你了。")
                
            if self.player_board.all_ships_sunk():
                self.game_phase = GamePhase.GAME_OVER
                self.update_status("💀 AI 獲勝了！")
                
        except Exception as e:
            self.update_status(f"⚠️ AI 策略載入錯誤: {e}")
            # Keep game running so user can fix the code
        finally:
            self.ai_turn_in_progress = False
            if self.game_phase == GamePhase.BATTLE:
                self.set_ai_cells_clickable(True)

if __name__ == "__main__":
    app = BattleshipArena()
    app.run()
