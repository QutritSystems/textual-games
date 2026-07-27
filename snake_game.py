#!/usr/bin/env python3
"""
Snake Game using Textual
A classic snake game where you eat food to grow and avoid hitting walls or yourself!

Controls:
- Arrow keys or WASD to move
- Q to quit
- R to restart
- P to pause/unpause
"""

import random
from enum import Enum
from typing import List, Tuple, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Label, Button, Header, Footer
from textual.reactive import reactive
from textual import events
from textual.timer import Timer


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class SnakeGame(App):
    """Snake game implementation."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .game-area {
        border: solid $primary;
        background: $panel;
        width: 52;
        height: 22;
        margin: 1;
    }
    
    .game-grid {
        background: $surface;
        color: $text;
        width: 50;
        height: 20;
    }
    
    .score-panel {
        border: solid $secondary;
        background: $panel;
        width: 52;
        height: 8;
        margin: 1;
        text-align: center;
    }
    
    .controls-panel {
        border: solid $accent;
        background: $panel;
        width: 52;
        height: 6;
        margin: 1;
        text-align: center;
    }
    
    Static {
        margin: 1;
    }
    
    Button {
        margin: 1;
    }
    """
    
    # Game state
    score = reactive(0)
    high_score = reactive(0)
    game_over = reactive(False)
    paused = reactive(False)
    
    def __init__(self):
        super().__init__()
        self.grid_width = 25
        self.grid_height = 10
        self.snake: List[Tuple[int, int]] = [(12, 5), (11, 5), (10, 5)]  # Start in middle
        self.direction = Direction.RIGHT
        self.food: Optional[Tuple[int, int]] = None
        self.game_timer: Optional[Timer] = None
        self.speed = 0.3  # seconds between moves
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Vertical():
            # Score panel
            with Container(classes="score-panel"):
                yield Static("🐍 SNAKE GAME 🐍", id="title")
                with Horizontal():
                    yield Label(f"Score: {self.score}", id="score")
                    yield Label(f"High Score: {self.high_score}", id="high-score")
                yield Label("READY TO START!", id="status")
            
            # Game area
            with Container(classes="game-area"):
                yield Static("", id="game-grid", classes="game-grid")
            
            # Controls panel
            with Container(classes="controls-panel"):
                yield Static("Arrow Keys/WASD: Move | P: Pause | R: Restart | Q: Quit")
                with Horizontal():
                    yield Button("Start Game", id="start", variant="success")
                    yield Button("Pause", id="pause", variant="warning")
                    yield Button("Restart", id="restart", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the game when the app starts."""
        self.spawn_food()
        self.update_display()
    
    def spawn_food(self) -> None:
        """Spawn food at a random location not occupied by snake."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def update_display(self) -> None:
        """Update the game display."""
        # Create empty grid (single-width chars only — emoji are double-width
        # and misalign the grid columns as the snake moves)
        grid = [['·' for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Place food
        if self.food:
            fx, fy = self.food
            grid[fy][fx] = '*'

        # Place snake
        for i, (x, y) in enumerate(self.snake):
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                if i == 0:  # Head
                    grid[y][x] = '@'
                else:  # Body
                    grid[y][x] = 'o'
        
        # Convert grid to string
        display = '\n'.join(''.join(row) for row in grid)
        self.query_one("#game-grid", Static).update(display)
        
        # Update score
        self.query_one("#score", Label).update(f"Score: {self.score}")
        self.query_one("#high-score", Label).update(f"High Score: {self.high_score}")
    
    def start_game(self) -> None:
        """Start or resume the game."""
        if self.game_over:
            self.reset_game()
        
        self.paused = False
        self.game_over = False
        
        if self.game_timer:
            self.game_timer.stop()
        
        self.game_timer = self.set_interval(self.speed, self.game_tick, name="game_timer")
        self.query_one("#status", Label).update("PLAYING!")
    
    def pause_game(self) -> None:
        """Pause or unpause the game."""
        if self.game_over:
            return
            
        self.paused = not self.paused
        
        if self.paused:
            if self.game_timer:
                self.game_timer.stop()
            self.query_one("#status", Label).update("PAUSED")
        else:
            self.game_timer = self.set_interval(self.speed, self.game_tick, name="game_timer")
            self.query_one("#status", Label).update("PLAYING!")
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        if self.game_timer:
            self.game_timer.stop()
        
        self.snake = [(12, 5), (11, 5), (10, 5)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.paused = False
        self.spawn_food()
        self.update_display()
        self.query_one("#status", Label).update("READY TO START!")
    
    def game_tick(self) -> None:
        """Main game loop - called every game tick."""
        if self.paused or self.game_over:
            return
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.end_game("Hit the wall!")
            return
        
        # Check self collision
        if new_head in self.snake:
            self.end_game("Hit yourself!")
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
            
            # Increase speed slightly
            self.speed = max(0.1, self.speed - 0.01)
            if self.game_timer:
                self.game_timer.stop()
            self.game_timer = self.set_interval(self.speed, self.game_tick, name="game_timer")
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        self.update_display()
    
    def end_game(self, reason: str) -> None:
        """End the game."""
        self.game_over = True
        if self.game_timer:
            self.game_timer.stop()
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.query_one("#status", Label).update(f"NEW HIGH SCORE! {reason}")
        else:
            self.query_one("#status", Label).update(f"GAME OVER! {reason}")
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard input."""
        if event.key == "q":
            self.exit()
        elif event.key == "r":
            self.reset_game()
        elif event.key == "p":
            self.pause_game()
        elif not self.game_over and not self.paused:
            # Direction controls
            if event.key in ("up", "w") and self.direction != Direction.DOWN:
                self.direction = Direction.UP
            elif event.key in ("down", "s") and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif event.key in ("left", "a") and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif event.key in ("right", "d") and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "start":
            self.start_game()
        elif event.button.id == "pause":
            self.pause_game()
        elif event.button.id == "restart":
            self.reset_game()


def main():
    """Run the Snake game."""
    print("🐍 Starting Snake Game...")
    print("Loading game...")
    
    app = SnakeGame()
    app.title = "Snake Game"
    app.run()


if __name__ == "__main__":
    main()
