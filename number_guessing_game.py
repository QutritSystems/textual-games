#!/usr/bin/env python3
"""
Number Guessing Game using Textual
Guess the secret number between 1 and 100!

Features:
- Hint system (too high/low)
- Attempt counter
- Difficulty levels
- High score tracking
"""

import random
import importlib.util
import hashlib
import asyncio
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    Static, Label, Button, Input, Header, Footer, 
    Select, ProgressBar
)
from textual.reactive import reactive
from textual import work
import number_guessing_strategies

class StrategyLoader:
    """Loads a changed strategy without mutating the currently active module."""

    def __init__(self, path: Path):
        self.path = path
        self._module = number_guessing_strategies
        self._fingerprint = self._fingerprint_file()

    def _fingerprint_file(self) -> str | None:
        try:
            return hashlib.sha256(self.path.read_bytes()).hexdigest()
        except OSError:
            return None

    def load(self):
        fingerprint = self._fingerprint_file()
        if fingerprint is None:
            return self._module
            
        if fingerprint == self._fingerprint:
            return self._module

        try:
            module_name = f"_guessing_strategy_{fingerprint}"
            spec = importlib.util.spec_from_file_location(module_name, self.path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Unable to load strategy from {self.path}")

            candidate = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(candidate)
            if not callable(getattr(candidate, "decide_guess", None)):
                raise TypeError("Strategy module must define decide_guess")

            self._module = candidate
            self._fingerprint = fingerprint
        except Exception as e:
            # Fallback to the last valid loaded module
            print(f"Error loading strategy: {e}")
            
        return self._module


class NumberGuessingGame(App):
    """Number guessing game with multiple difficulty levels."""
    
    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    
    .game-container {
        border: solid $primary;
        background: $panel;
        width: 65;
        height: auto;
        max-height: 100vh;
        overflow-y: auto;
        margin: 0;
        padding: 0 1;
    }
    
    .title {
        text-align: center;
        background: $secondary;
        color: $text;
        margin-bottom: 0;
        padding: 0;
    }
    
    .game-info {
        background: $surface;
        margin: 0;
        padding: 0;
        text-align: center;
        height: auto;
    }
    
    .difficulty-area {
        margin: 0;
        padding: 0;
        text-align: center;
        height: auto;
    }
    
    .input-area {
        background: $panel;
        margin: 0;
        padding-bottom: 1;
        text-align: center;
        height: auto;
    }
    
    .input-area Horizontal {
        height: 3;
        align: center middle;
        margin-top: 1;
    }
    
    .hint-area {
        background: $warning;
        color: $text;
        margin: 0;
        padding: 0;
        text-align: center;
        height: auto;
        min-height: 2;
    }
    
    .stats {
        background: $success;
        color: $text;
        margin: 0;
        padding: 0;
        text-align: center;
        height: auto;
    }
    
    Button {
        margin: 0 1;
    }
    
    Input {
        margin: 0;
        width: 100%;
    }
    
    Select {
        margin: 0;
        width: 100%;
    }
    
    ProgressBar {
        margin: 0;
    }
    """
    
    # Game state
    secret_number = reactive(0)
    attempts = reactive(0)
    max_attempts = reactive(10)
    game_over = reactive(False)
    won = reactive(False)
    difficulty = reactive("Medium")
    min_number = reactive(1)
    max_number = reactive(100)
    best_score = reactive(999)
    
    def __init__(self):
        super().__init__()
        self.guesses = []
        self.difficulty_settings = {
            "Easy": (1, 50, 15),      # min, max, attempts
            "Medium": (1, 100, 10),
            "Hard": (1, 200, 7),
            "Expert": (1, 500, 5)
        }
        self.auto_ai_running = False
        self.auto_ai_worker = None
        self.auto_ai_generation = 0
        self.strategy_loader = StrategyLoader(Path(number_guessing_strategies.__file__).resolve())
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="game-container"):
            yield Static("🎯 NUMBER GUESSING GAME 🎯", classes="title")
            
            # Game info panel
            with Container(classes="game-info"):
                yield Label(f"Guess the number between {self.min_number} and {self.max_number}!", id="range-info")
                yield Label(f"Attempts remaining: {self.max_attempts - self.attempts}", id="attempts-info")
                yield ProgressBar(total=self.max_attempts, id="progress")
            
            # Difficulty selection
            with Container(classes="difficulty-area"):
                yield Label("Difficulty Level:", id="difficulty-label")
                yield Select([
                    ("Easy (1-50, 15 attempts)", "Easy"),
                    ("Medium (1-100, 10 attempts)", "Medium"), 
                    ("Hard (1-200, 7 attempts)", "Hard"),
                    ("Expert (1-500, 5 attempts)", "Expert")
                ], value="Medium", id="difficulty-select")
            
            # Input area
            with Container(classes="input-area"):
                yield Label("Enter Your Guess:", id="input-label")
                yield Input(placeholder="Enter your guess...", id="guess-input", type="integer")
                with Horizontal():
                    yield Button("Submit Guess", id="submit", variant="primary")
                    yield Button("New Game", id="new-game", variant="success")
                    yield Button("Give Up", id="give-up", variant="error")
                    yield Button("AI 玩一局", id="start-ai", variant="warning")
                    yield Button("停止 AI", id="stop-ai", variant="default", disabled=True)
            
            # Hint area
            with Container(classes="hint-area"):
                yield Label("Make your first guess!", id="hint")
                yield Label("", id="guess-history")
            
            # Stats panel
            with Container(classes="stats"):
                yield Label(f"Best Score: {self.best_score if self.best_score < 999 else 'None'}", id="best-score")
                yield Label(f"Current Difficulty: {self.difficulty}", id="current-difficulty")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize game when app starts."""
        self.new_game()
        
    async def on_unmount(self) -> None:
        if self.auto_ai_worker:
            self.auto_ai_worker.cancel()
            await self.auto_ai_worker.wait()
        
    def new_game(self) -> None:
        """Start a new game."""
        # Get difficulty settings
        min_num, max_num, max_att = self.difficulty_settings[self.difficulty]
        self.min_number = min_num
        self.max_number = max_num
        self.max_attempts = max_att
        
        # Reset game state
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        self.game_over = False
        self.won = False
        self.guesses = []
        
        # Update UI
        self.query_one("#range-info", Label).update(
            f"Guess the number between {self.min_number} and {self.max_number}!"
        )
        self.query_one("#attempts-info", Label).update(
            f"Attempts remaining: {self.max_attempts - self.attempts}"
        )
        self.query_one("#hint", Label).update("Make your first guess!")
        self.query_one("#guess-history", Label).update("")
        self.query_one("#guess-input", Input).value = ""
        
        # Reset progress bar
        progress_bar = self.query_one("#progress", ProgressBar)
        progress_bar.total = self.max_attempts
        progress_bar.progress = 0
        
        # Update difficulty display
        self.query_one("#current-difficulty", Label).update(f"Current Difficulty: {self.difficulty}")
        
        self.notify(f"New {self.difficulty} game started! Good luck! 🍀")
        self.query_one("#guess-input", Input).focus()
    
    def make_guess(self, guess: int) -> None:
        """Process a guess."""
        if self.game_over:
            return
        
        self.attempts += 1
        self.guesses.append(guess)
        
        # Update progress bar
        progress_bar = self.query_one("#progress", ProgressBar)
        progress_bar.progress = self.attempts
        
        # Update attempts counter
        remaining = self.max_attempts - self.attempts
        self.query_one("#attempts-info", Label).update(f"Attempts remaining: {remaining}")
        
        # Check guess
        if guess == self.secret_number:
            self.win_game()
        elif guess < self.secret_number:
            hint = f"📈 Too low! Try higher than {guess}"
            if remaining > 0:
                self.query_one("#hint", Label).update(hint)
            else:
                self.lose_game()
        else:  # guess > secret_number
            hint = f"📉 Too high! Try lower than {guess}"
            if remaining > 0:
                self.query_one("#hint", Label).update(hint)
            else:
                self.lose_game()
        
        # Update guess history (show last 5 guesses)
        recent_guesses = self.guesses[-5:]
        history = "Recent guesses: " + " → ".join(map(str, recent_guesses))
        self.query_one("#guess-history", Label).update(history)
        
        # Check if out of attempts
        if remaining == 0 and not self.won:
            self.lose_game()
    
    def win_game(self) -> None:
        """Handle winning the game."""
        self.won = True
        self.game_over = True
        
        # Update best score
        if self.attempts < self.best_score:
            self.best_score = self.attempts
            self.query_one("#best-score", Label).update(f"Best Score: {self.best_score}")
            self.query_one("#hint", Label).update(
                f"🎉 CONGRATULATIONS! You found {self.secret_number} in {self.attempts} attempts! NEW RECORD! 🏆"
            )
            self.notify("🏆 NEW PERSONAL RECORD! 🏆")
        else:
            self.query_one("#hint", Label).update(
                f"🎉 CONGRATULATIONS! You found {self.secret_number} in {self.attempts} attempts!"
            )
            self.notify("🎉 You won! Great job! 🎉")
    
    def lose_game(self) -> None:
        """Handle losing the game."""
        self.game_over = True
        self.query_one("#hint", Label).update(
            f"😔 Game Over! The number was {self.secret_number}. Better luck next time!"
        )
        self.notify("😔 Better luck next time!")
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle difficulty selection change."""
        if event.select.id == "difficulty-select":
            self.difficulty = event.value
            self.new_game()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "guess-input":
            self.submit_guess()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "submit":
            self.submit_guess()
        elif event.button.id == "new-game":
            self.new_game()
            if self.auto_ai_running:
                self.stop_ai_guesser()
        elif event.button.id == "give-up":
            if not self.game_over:
                self.lose_game()
            if self.auto_ai_running:
                self.stop_ai_guesser()
        elif event.button.id == "start-ai":
            if self.auto_ai_running:
                return
            if self.game_over:
                self.new_game()
                
            self.auto_ai_running = True
            self.query_one("#start-ai", Button).disabled = True
            self.query_one("#stop-ai", Button).disabled = False
            self.query_one("#submit", Button).disabled = True
            self.query_one("#give-up", Button).disabled = True
            self.query_one("#difficulty-select").disabled = True
            self.query_one("#guess-input", Input).disabled = True
            
            self.auto_ai_generation += 1
            self.auto_ai_worker = self.run_ai_guesser(self.auto_ai_generation)
            
        elif event.button.id == "stop-ai":
            self.stop_ai_guesser()
            
    def stop_ai_guesser(self) -> None:
        self.auto_ai_running = False
        if self.auto_ai_worker:
            self.auto_ai_worker.cancel()
            self.auto_ai_worker = None
        self.query_one("#start-ai", Button).disabled = False
        self.query_one("#stop-ai", Button).disabled = True
        self.query_one("#submit", Button).disabled = False
        self.query_one("#give-up", Button).disabled = False
        self.query_one("#difficulty-select").disabled = False
        self.query_one("#guess-input", Input).disabled = False
        self.query_one("#guess-input", Input).focus()

    @work(group="auto_guess", exclusive=True)
    async def run_ai_guesser(self, generation: int) -> None:
        try:
            while self.auto_ai_running and not self.game_over:
                self.query_one("#hint", Label).update("🤖 AI 正在精密計算下一手最優解...")
                await asyncio.sleep(0.6)
                
                if not self.auto_ai_running or self.game_over:
                    break
                    
                strategy_module = self.strategy_loader.load()
                
                history = []
                for g in self.guesses:
                    if g < self.secret_number:
                        history.append((g, "low"))
                    elif g > self.secret_number:
                        history.append((g, "high"))
                        
                guess, reasoning = strategy_module.decide_guess(self.min_number, self.max_number, history)
                
                self.query_one("#hint", Label).update(reasoning)
                await asyncio.sleep(0.8)
                
                if not self.auto_ai_running or self.game_over:
                    break
                    
                self.make_guess(guess)
                await asyncio.sleep(0.6)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.query_one("#hint", Label).update(f"⚠️ AI 發生錯誤: {e}")
        finally:
            if self.auto_ai_generation == generation:
                self.auto_ai_running = False
                self.auto_ai_worker = None
                self.query_one("#start-ai", Button).disabled = False
                self.query_one("#stop-ai", Button).disabled = True
                self.query_one("#submit", Button).disabled = False
                self.query_one("#give-up", Button).disabled = False
                self.query_one("#difficulty-select").disabled = False
                self.query_one("#guess-input", Input).disabled = False
                self.query_one("#guess-input", Input).focus()
    
    def submit_guess(self) -> None:
        """Submit the current guess."""
        if self.game_over:
            return
            
        guess_input = self.query_one("#guess-input", Input)
        
        try:
            guess = int(guess_input.value)
            if self.min_number <= guess <= self.max_number:
                self.make_guess(guess)
                guess_input.value = ""  # Clear input
            else:
                self.query_one("#hint", Label).update(
                    f"❌ Please enter a number between {self.min_number} and {self.max_number}!"
                )
        except ValueError:
            self.query_one("#hint", Label).update("❌ Please enter a valid number!")
            
        guess_input.focus()


def main():
    """Run the Number Guessing game."""
    print("🎯 Starting Number Guessing Game...")
    print("Loading game...")
    
    app = NumberGuessingGame()
    app.title = "Number Guessing Game"
    app.run()


if __name__ == "__main__":
    main()
