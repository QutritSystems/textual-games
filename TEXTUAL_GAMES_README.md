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
Centralized launcher for all games with a beautiful interface!

**Features:**
- Visual game selection menu
- Game descriptions and previews
- Keyboard shortcuts (1, 2, Q)
- Clean, modern UI design

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- Textual library

### Installation Steps

1. **Create virtual environment**:
   ```bash
   python3 -m venv textual-env
   source textual-env/bin/activate
   ```

2. **Install Textual**:
   ```bash
   pip install "textual[dev]>=0.45.0"
   ```

3. **Run games**:
   ```bash
   # Launch game selector
   python game_launcher.py
   
   # Or run games directly
   python snake_game.py
   python number_guessing_game.py
   ```

## 🎮 How to Play / 如何遊玩

### Quick Start / 快速開始
```bash
# 進入遊戲資料夾 / Navigate to games directory
cd textual-games

# 使用便捷腳本 / Use convenience script
./play.sh launcher    # 啟動遊戲選擇器 / Start game launcher
./play.sh snake      # 直接啟動貪食蛇 / Direct launch Snake Game
./play.sh guess      # 直接啟動猜數字 / Direct launch Number Guessing
```

### Manual Launch / 手動啟動
```bash
# 激活虛擬環境 / Activate virtual environment
source ../textual-env/bin/activate

# 啟動遊戲 / Launch games
python game_launcher.py      # 遊戲選擇器 / Game launcher
python snake_game.py         # 貪食蛇遊戲 / Snake Game
python number_guessing_game.py # 猜數字遊戲 / Number Guessing Game
```

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
