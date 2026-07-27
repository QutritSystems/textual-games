import asyncio
from textual.widgets import Button
from battleship_arena import BattleshipArena
from battleship_core import CellState, GamePhase, GameMode

async def test_auto_battle_integration() -> None:
    app = BattleshipArena()
    async with app.run_test() as pilot:
        start_btn = app.query_one("#start-ai-battle")
        
        # Direct message dispatch
        print("Dispatching Button.Pressed directly...")
        await app.on_button_pressed(Button.Pressed(start_btn))
        await pilot.pause()
        
        print("After dispatch game_phase:", app.game_phase)
        print("After dispatch game_mode:", app.game_mode)
        print("After dispatch auto_battle_running:", app.auto_battle_running)
        
        # Wait a bit and check grid
        await pilot.pause(1.5)
        
        p1_attacks = sum(1 for r in range(10) for c in range(10) if app.ai_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK})
        p2_attacks = sum(1 for r in range(10) for c in range(10) if app.player_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK})
        print(f"Attacks: P1={p1_attacks}, P2={p2_attacks}")

if __name__ == "__main__":
    asyncio.run(test_auto_battle_integration())
