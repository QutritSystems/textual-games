import asyncio

from textual.widgets import Button

from battleship_arena import BattleshipArena, GridCell
from battleship_core import CellState, GamePhase, GameMode


async def test_click_message_targets_ai_grid() -> None:
    app = BattleshipArena()
    async with app.run_test() as pilot:
        await app.on_button_pressed(Button.Pressed(app.query_one("#auto-place")))
        await app.on_button_pressed(Button.Pressed(app.query_one("#start-battle")))

        cell = app.ai_grid.cells[0][0]
        assert app.game_phase == GamePhase.BATTLE
        assert cell.clickable

        cell.on_click()
        await pilot.pause()

        assert app.ai_board.grid[0][0] in {
            CellState.MISS,
            CellState.HIT,
            CellState.SUNK,
        }


def test_click_message_exposes_source_control() -> None:
    cell = GridCell(0, 0)
    message = cell.CellClicked(0, 0, cell)
    assert message.control is cell

async def test_auto_battle_start_and_stop() -> None:
    app = BattleshipArena()
    async with app.run_test() as pilot:
        start_btn = app.query_one("#start-ai-battle")
        stop_btn = app.query_one("#stop-battle")
        
        # Start AI vs AI
        await app.on_button_pressed(Button.Pressed(start_btn))
        assert app.game_phase == GamePhase.BATTLE
        assert app.game_mode == GameMode.AI_VS_AI
        assert app.auto_battle_running is True
        
        # Both grids should be locked from manual clicking
        assert not app.player_grid.clickable
        assert not app.ai_grid.clickable
        
        # Wait a brief moment for the worker to take at least one turn
        await asyncio.sleep(0.5)
        await pilot.pause()
        
        # Stop Battle
        await app.on_button_pressed(Button.Pressed(stop_btn))
        assert app.game_phase == GamePhase.GAME_OVER
        assert app.game_mode == GameMode.MANUAL
        assert app.auto_battle_running is False
        
        # Ensure worker completes cancellation
        await pilot.pause()

if __name__ == "__main__":
    asyncio.run(test_click_message_targets_ai_grid())
    test_click_message_exposes_source_control()
    asyncio.run(test_auto_battle_start_and_stop())
    print("Arena tests passed!")
