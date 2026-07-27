import asyncio
from number_guessing_game import NumberGuessingGame

async def test():
    app = NumberGuessingGame()
    async with app.run_test() as pilot:
        # Print children of the game container
        container = app.query_one(".game-container")
        print("Game container children:")
        for child in container.children:
            print(f"- {child.__class__.__name__} (id={child.id}, classes={child.classes}, visible={child.visible}, size={child.size})")
            # If it's a container, let's see its nested children
            if hasattr(child, "children") and child.children:
                print("  Nested:")
                for nested in child.children:
                    print(f"  * {nested.__class__.__name__} (id={nested.id}, visible={nested.visible}, size={nested.size})")

if __name__ == "__main__":
    asyncio.run(test())
