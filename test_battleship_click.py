import asyncio
from final_battleship import FinalBattleshipGame

async def simulate():
    app = FinalBattleshipGame()
    async with app.run_test() as pilot:
        # Auto-place ships for player
        await pilot.click("#auto-place")
        await pilot.pause()
        
        # Start battle
        await pilot.click("#start-battle")
        await pilot.pause()
        
        # Click on cell (0, 0) of AI grid
        ai_grid = app.ai_grid
        cell = ai_grid.cells[0][0]
        print("Before click, cell state:", cell.cell_state)
        await pilot.click(cell.__class__) # Wait, let's just call the event handler
        
        # Or manually post message
        cell.post_message(cell.CellClicked(0, 0))
        await pilot.pause()
        
        print("Cell state in board after attack:", app.ai_board.grid[0][0])
        print("Cell display state:", cell.cell_state)
        print("Cell text:", cell.render())
        print("Cell color:", cell.styles.color)

if __name__ == "__main__":
    asyncio.run(simulate())
