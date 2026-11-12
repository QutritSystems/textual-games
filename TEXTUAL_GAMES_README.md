# 🎮 Textual Games Collection

A collection of fun terminal-based games built with [Textual](https://textual.textualize.io/), a modern Python framework for building rich text user interfaces.

## 🎯 Games Included

### 🐍 Snake Game (`snake_game.py`)
Classic arcade snake game with modern terminal UI!

**Features:**
- Smooth gameplay with emoji graphics (🟢 snake head, 🟨 snake body, 🍎 food)
- Arrow keys or WASD controls
- Increasing difficulty as you score
- Score tracking and high score system
- Pause/resume functionality
- Real-time collision detection

**Controls:**
- **Movement**: Arrow keys or WASD
- **Pause**: P key
- **Restart**: R key  
- **Quit**: Q key
- **Buttons**: Start Game, Pause, Restart

**How to Play:**
1. Click "Start Game" or press any arrow key
2. Guide the snake to eat the red apples 🍎
3. Avoid hitting walls or your own tail
4. Score increases by 10 for each apple eaten
5. Snake gets faster as you progress

### 🎯 Number Guessing Game (`number_guessing_game.py`)
Strategic number guessing game with multiple difficulty levels!

**Features:**
- 4 difficulty levels (Easy to Expert)
- Smart hint system (too high/low guidance)
- Progress bar showing attempts used
- Guess history tracking
- Personal best score tracking
- Input validation and error handling

**Difficulty Levels:**
- **Easy**: 1-50, 15 attempts
- **Medium**: 1-100, 10 attempts  
- **Hard**: 1-200, 7 attempts
- **Expert**: 1-500, 5 attempts

**How to Play:**
1. Select your difficulty level
2. Enter a number within the range
3. Use the hints to narrow down your guesses
4. Try to find the number in fewer attempts
5. Beat your personal best score!

### 🚀 Game Launcher (`game_launcher.py`)
Centralized launcher for the playable games with a visual interface.

**Features:**
- Visual game selection menu
- Game descriptions and previews
- Keyboard shortcuts (1–4, Q)
- Starts games with the same Python interpreter as the launcher

### 🚢 Battleship (`battleship_game.py`)
A turn-based Battleship game against an AI opponent.

### 🤖 Battleship AI Arena (`battleship_arena.py`)
A sandbox for running and hot-reloading the strategies in
`battleship_strategies.py`.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or newer
- A POSIX shell (only needed for `play.sh`)

### Quick start

From the repository root, create an isolated environment and install the
version-pinned runtime and development dependencies:

```bash
./play.sh setup
./play.sh test
./play.sh launcher
```

`setup` creates `.venv` in the repository. It is ignored by Git, and every
subsequent `play.sh` command uses it automatically. `requirements.txt` pins the
runtime; `requirements-dev.txt` adds the pinned development tooling, including
pre-commit.

### Manual setup

Use this on Windows or when you do not want to use the shell launcher:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --requirement requirements-dev.txt
.venv/bin/python test_all_games.py
.venv/bin/python test_core.py
.venv/bin/python test_battleship_arena.py
.venv/bin/python test_auto_battle_logic.py
.venv/bin/python test_number_guessing_ai.py
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`.

To enable the repository hooks after setup:

```bash
.venv/bin/pre-commit install
```

## 🎮 How to Play / 如何遊玩

```bash
./play.sh launcher    # 遊戲選擇器
./play.sh snake       # 貪食蛇
./play.sh guess       # 猜數字
./play.sh ascii       # ASCII 藝術產生器
./play.sh battleship  # 潛艇對決
./play.sh arena       # Battleship AI Arena
```

All commands can be run from any current working directory because the script
resolves its own location. To select a different interpreter, set `PYTHON`,
for example: `PYTHON=python3.12 ./play.sh test`.


## 🎨 Technical Features

### Textual Framework Showcase
These games demonstrate various Textual capabilities:

- **Reactive Variables**: Real-time state updates
- **Custom CSS Styling**: Beautiful terminal interfaces
- **Event Handling**: Keyboard and mouse input
- **Layout Containers**: Responsive UI design
- **Widget Library**: Buttons, inputs, progress bars, etc.
- **Timer System**: Game loops and animations
- **Notifications**: User feedback system

### Code Highlights
- **Object-Oriented Design**: Clean, maintainable code structure
- **Type Hints**: Full type annotation for better development experience  
- **Error Handling**: Robust input validation and error management
- **Modular Architecture**: Easily extensible for new games
- **Performance Optimized**: Efficient rendering and game loops

## 📁 File Structure
```
textual-games/
├── snake_game.py              # Snake game implementation
├── number_guessing_game.py    # Number guessing game
├── game_launcher.py           # Game selection interface
├── TEXTUAL_GAMES_README.md    # This documentation
└── textual-env/               # Python virtual environment
```

## 🎪 Game Screenshots (ASCII Art)

### Snake Game
```
┌─────────────────────────────┐
│       🐍 SNAKE GAME 🐍      │
├─────────────────────────────┤
│ Score: 50    High: 120      │
│ ························🍎·· │
│ ························   │
│ ·····🟨🟨🟢················ │
│ ························   │
│ ························   │
└─────────────────────────────┘
```

### Number Guessing Game
```
┌──────────────────────────────┐
│    🎯 NUMBER GUESSING 🎯     │
├──────────────────────────────┤
│ Guess between 1 and 100!    │
│ Attempts: [██████░░░░] 6/10  │
│ 📈 Too low! Try higher > 45  │
│ Recent: 25 → 60 → 35 → 45    │
└──────────────────────────────┘
```

## 🔧 Customization

### Adding New Games
1. Create a new Python file with Textual App class
2. Add game entry to `game_launcher.py`
3. Follow the existing pattern for consistency

### Modifying Difficulty
Edit the `difficulty_settings` dictionary in `number_guessing_game.py`:
```python
self.difficulty_settings = {
    "Custom": (min_val, max_val, attempts),
    # Add your custom difficulty here
}
```

### Styling Changes
Modify the `CSS` string in each game class to customize appearance.

## 🚀 Future Enhancements

Planned features for future versions:
- 🎲 **Dice Games**: Yahtzee, dice poker
- 🧩 **Puzzle Games**: Sliding puzzles, word games  
- 🎯 **Arcade Games**: Breakout, space invaders
- 🃏 **Card Games**: Solitaire, blackjack
- 💾 **Save System**: Persistent high scores and settings
- 🌈 **Themes**: Multiple color themes and styles
- 🔊 **Sound Effects**: Terminal bell sounds for actions
- 👥 **Multiplayer**: Local multiplayer support

## 🐛 Troubleshooting

### Common Issues

**"No module named 'textual'"**
```bash
# Make sure virtual environment is activated
source textual-env/bin/activate
pip install "textual[dev]>=0.45.0"
```

**Game doesn't respond to keyboard**
- Make sure the terminal window has focus
- Try clicking on the game area first
- Some terminals may require enabling mouse support

**Visual glitches**  
- Try resizing your terminal window
- Ensure your terminal supports emoji and Unicode
- Modern terminals (iTerm2, Windows Terminal) work best

## 📚 Learning Resources

- [Textual Documentation](https://textual.textualize.io/)
- [Textual Tutorial](https://textual.textualize.io/tutorial/)
- [Python Game Development](https://realpython.com/python-game-development/)

## 🎉 Enjoy Gaming!

Have fun playing these terminal games! They showcase the power of modern terminal interfaces while providing classic gaming entertainment.

**Happy Gaming!** 🎮✨
