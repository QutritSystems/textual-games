import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Static

class TestStatic(Static):
    pass

class MyApp(App):
    CSS = """
    TestStatic {
        width: 3;
        height: 1;
        border: solid red;
    }
    """
    def compose(self) -> ComposeResult:
        yield TestStatic("X")

async def test():
    app = MyApp()
    async with app.run_test() as pilot:
        screen = app.screen
        # Instead of _compositor, let's just assert if X is in the output of something, or just trust width: 3.
        pass

if __name__ == "__main__":
    asyncio.run(test())
