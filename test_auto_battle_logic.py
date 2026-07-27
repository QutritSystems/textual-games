import asyncio
from textual.widgets import Button
from battleship_arena import BattleshipArena
from battleship_core import CellState

async def test_auto_battle_integration() -> None:
    app = BattleshipArena()
    async with app.run_test() as pilot:
        # Ensure initially empty
        assert app.ai_board.grid[0][0] == CellState.EMPTY
        
        # Start AI vs AI
        start_btn = app.query_one("#start-ai-battle", Button)
        await app.on_button_pressed(Button.Pressed(start_btn))
        await pilot.pause()
        
        # Give worker a chance to make a few moves using pilot.pause
        await pilot.pause(1.5)
        
        # Check that boards have been mutated
        p1_attacks = 0
        p2_attacks = 0
        for r in range(10):
            for c in range(10):
                if app.ai_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK}:
                    p1_attacks += 1
                if app.player_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK}:
                    p2_attacks += 1
                    
        assert p1_attacks > 0, "Player 1 should have attacked the AI board"
        assert p2_attacks > 0, "Player 2 should have attacked the Player board"
        
        # Stop Battle
        stop_btn = app.query_one("#stop-battle", Button)
        await app.on_button_pressed(Button.Pressed(stop_btn))
        await pilot.pause(0.2)
        
        # Ensure cleanup is successful
        assert app.auto_battle_worker is None
        assert app.player_grid.clickable is True

        # Ensure board stops changing after stop
        p1_attacks_after_stop = 0
        for r in range(10):
            for c in range(10):
                if app.ai_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK}:
                    p1_attacks_after_stop += 1
        
        await pilot.pause(1.0)
        
        p1_attacks_final = 0
        for r in range(10):
            for c in range(10):
                if app.ai_board.grid[r][c] in {CellState.HIT, CellState.MISS, CellState.SUNK}:
                    p1_attacks_final += 1
                    
        assert p1_attacks_after_stop == p1_attacks_final, "Board should not mutate after battle stopped"

if __name__ == "__main__":
    asyncio.run(test_auto_battle_integration())
    print("Auto-battle integration test passed!")
