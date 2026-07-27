import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Static

class TestStatic(Static):
    def on_mount(self):
        self.set_interval(1, self.tick)
        self.count = 0
    def tick(self):
        self.count += 1
        self.update(f"Tick {self.count}")
        if self.count % 2 == 0:
            self.styles.color = "red"
        else:
            self.styles.color = "blue"
        if self.count == 3:
            self.app.exit(0)

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield TestStatic("Initial")

if __name__ == "__main__":
    app = MyApp()
    app.run()
