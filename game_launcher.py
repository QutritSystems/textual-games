#!/usr/bin/env python3
"""
Textual Games Launcher
Choose from multiple games built with Textual!
"""

import subprocess
import sys
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Header, Footer, Label
from textual import events


class GameLauncher(App):
    """Main game launcher interface."""
    
    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    
    .launcher {
        border: solid $primary;
        background: $panel;
        width: 80;
        max-height: 90vh;
        margin: 1;
        padding: 1;
    }
    
    .title {
        text-align: center;
        background: $secondary;
        color: $text;
        margin: 1 0;
        padding: 1;
    }
    
    .game-grid {
        margin: 1;
        padding: 1;
        height: auto;
    }
    
    .game-card {
        border: solid $accent;
        background: $surface;
        margin: 1 0;
        padding: 1;
        height: auto;
        min-height: 8;
        text-align: center;
    }
    
    .game-title {
        background: $primary;
        color: $text;
        text-align: center;
        margin-bottom: 1;
        padding: 1;
    }
    
    .game-desc {
        text-align: center;
        margin: 1;
        padding: 0 1;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    
    .footer-info {
        text-align: center;
        background: $warning;
        margin: 1 0;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="launcher"):
            yield Static("🎮 TEXTUAL GAMES LAUNCHER 🎮", classes="title")
            
            with Vertical(classes="game-grid"):
                # Snake Game
                with Container(classes="game-card"):
                    yield Static("🐍 Snake Game", classes="game-title")
                    yield Static("Classic snake game!\nEat food, grow longer,\navoid walls and yourself!", classes="game-desc")
                    yield Button("Play Snake", id="snake", variant="success")
                
                # Number Guessing Game  
                with Container(classes="game-card"):
                    yield Static("🎯 Number Guessing", classes="game-title")
                    yield Static("Guess the secret number!\nMultiple difficulty levels,\nbeat your high score!", classes="game-desc")
                    yield Button("Play Guessing", id="guessing", variant="primary")
                
                # ASCII Art Generator
                with Container(classes="game-card"):
                    yield Static("🎨 ASCII Art Generator", classes="game-title")
                    yield Static("Create beautiful ASCII art!\nMultiple font styles,\nborders and effects!", classes="game-desc")
                    yield Button("Create ASCII Art", id="ascii-art", variant="primary")
                
                # Battleship Game
                with Container(classes="game-card"):
                    yield Static("🚢 潛艇對決", classes="game-title")
                    yield Static("戰艦對戰遊戲！\n智能 AI 對手，\n策略性回合制戰鬥！", classes="game-desc")
                    yield Button("開始潛艇對決", id="battleship", variant="error")
                
                # Coming Soon placeholder
                with Container(classes="game-card"):
                    yield Static("🚀 More Games", classes="game-title")
                    yield Static("More games coming soon!\nTic-tac-toe, memory game,\nword puzzles and more!", classes="game-desc")
                    yield Button("Coming Soon", id="coming-soon", variant="warning", disabled=True)
            
            yield Static("Press Q to quit | Click a game to start playing!", classes="footer-info")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle game selection."""
        if event.button.id == "snake":
            self.launch_game("snake_game.py", "Snake Game")
        elif event.button.id == "guessing":
            self.launch_game("number_guessing_game.py", "Number Guessing Game")
        elif event.button.id == "ascii-art":
            self.launch_game("ascii_art_generator.py", "ASCII Art Generator")
        elif event.button.id == "battleship":
            self.launch_game("battleship_game.py", "潛艇對決")
        elif event.button.id == "coming-soon":
            self.notify("More games coming soon! Stay tuned! 🚀")
    
    def launch_game(self, game_file: str, game_name: str) -> None:
        """Launch a game in a new process."""
        try:
            self.notify(f"Starting {game_name}...")
            
            # Exit this launcher
            self.exit()
            
            # Start the game
            subprocess.run([
                "/Users/databird/textual-env/bin/python", 
                f"/Users/databird/textual-games/{game_file}"
            ])
            
        except Exception as e:
            self.notify(f"Error launching {game_name}: {e}")
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts."""
        if event.key == "q":
            self.exit()
        elif event.key == "1":
            self.launch_game("snake_game.py", "Snake Game")
        elif event.key == "2":
            self.launch_game("number_guessing_game.py", "Number Guessing Game")
        elif event.key == "3":
            self.launch_game("ascii_art_generator.py", "ASCII Art Generator")
        elif event.key == "4":
            self.launch_game("battleship_game.py", "潛艇對決")


def main():
    """Run the game launcher."""
    print("🎮 Starting Textual Games Launcher...")
    print("Available games:")
    print("  🐍 Snake Game - Classic arcade action")
    print("  🎯 Number Guessing - Mind puzzle challenge")
    print()
    
    app = GameLauncher()
    app.title = "Textual Games"
    app.run()


if __name__ == "__main__":
    main()
