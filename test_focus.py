import asyncio
from number_guessing_game import NumberGuessingGame

async def test():
    app = NumberGuessingGame()
    async with app.run_test() as pilot:
        print("Focused widget in original game:", app.focused)

if __name__ == "__main__":
    asyncio.run(test())
