import asyncio
from textual.widgets import Button
from number_guessing_game import NumberGuessingGame

async def test_guessing_ai_integration() -> None:
    app = NumberGuessingGame()
    async with app.run_test() as pilot:
        # Initial state checks
        assert app.secret_number > 0
        assert app.attempts == 0
        assert app.won is False
        assert app.game_over is False
        
        # Start AI Auto Guessing
        start_btn = app.query_one("#start-ai", Button)
        await app.on_button_pressed(Button.Pressed(start_btn))
        await pilot.pause()
        
        # Verify AI is running
        assert app.auto_ai_running is True
        assert app.auto_ai_worker is not None
        
        # Give Binary Search a few virtual seconds to solve the game.
        # Since Easy (1-50) is default, Binary Search is mathematically guaranteed 
        # to solve it within 6 attempts (each attempt takes ~2.0s virtual time in sleep)
        print("Letting AI play...")
        await pilot.pause(10.0)
        
        # Verify that the game has ended and AI won!
        print(f"Attempts: {app.attempts}, won: {app.won}, game_over: {app.game_over}")
        assert app.won is True, "Binary Search should mathematically win the game"
        assert app.game_over is True
        assert app.auto_ai_running is False
        assert app.auto_ai_worker is None

if __name__ == "__main__":
    asyncio.run(test_guessing_ai_integration())
    print("Number guessing AI integration test passed!")
