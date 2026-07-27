import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Label

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Label("Test Message", id="test-label")

async def test():
    app = MyApp()
    async with app.run_test() as pilot:
        label = app.query_one("#test-label")
        print("label attributes:", dir(label))
        print("label.renderable:", getattr(label, "renderable", "NOT FOUND"))
        print("label._renderable:", getattr(label, "_renderable", "NOT FOUND"))

if __name__ == "__main__":
    asyncio.run(test())
