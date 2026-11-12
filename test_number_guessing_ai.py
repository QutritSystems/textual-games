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

        # Use the first binary-search guess so this test verifies the integration
        # without depending on random state or an arbitrary worker timeout.
        app.secret_number = 50

        # Start AI Auto Guessing
        start_btn = app.query_one("#start-ai", Button)
        await app.on_button_pressed(Button.Pressed(start_btn))
        await pilot.pause()

        # Verify AI is running
        assert app.auto_ai_running is True
        assert app.auto_ai_worker is not None

        # The default Medium range has 50 as its first binary-search guess.
        # Wait for the worker's UI delays and one completed guess.
        print("Letting AI play...")
        await pilot.pause(3.0)

        # Verify that the game has ended and AI won!
        print(f"Attempts: {app.attempts}, won: {app.won}, game_over: {app.game_over}")
        assert app.won is True, "Binary Search should mathematically win the game"
        assert app.game_over is True
        assert app.auto_ai_running is False
        assert app.auto_ai_worker is None


if __name__ == "__main__":
    asyncio.run(test_guessing_ai_integration())
    print("Number guessing AI integration test passed!")
