#!/usr/bin/env bash
# Portable launcher for the Textual Games collection.

set -eu

PROJECT_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

if [ "${PYTHON:-}" != "" ]; then
    PYTHON_BIN="$PYTHON"
elif [ -x "$VENV_DIR/bin/python" ]; then
    PYTHON_BIN="$VENV_DIR/bin/python"
else
    PYTHON_BIN="python3"
fi

usage() {
    cat <<'EOF'
🎮 Textual Games Collection

Usage:
  ./play.sh setup       Create .venv and install pinned dependencies
  ./play.sh test        Run the full automated test suite
  ./play.sh launcher    Start the game selector
  ./play.sh snake       Play Snake
  ./play.sh guess       Play Number Guessing
  ./play.sh ascii       Start the ASCII Art Generator
  ./play.sh battleship  Play Battleship
  ./play.sh arena       Start the Battleship AI Arena

Set PYTHON=/path/to/python to use a specific interpreter.
EOF
}

setup() {
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    "$VENV_DIR/bin/python" -m pip install --upgrade pip
    "$VENV_DIR/bin/python" -m pip install --requirement "$PROJECT_DIR/requirements-dev.txt"
}

require_dependencies() {
    if ! "$PYTHON_BIN" -c 'import textual' >/dev/null 2>&1; then
        echo "❌ Textual is not installed for $PYTHON_BIN. Run: ./play.sh setup" >&2
        exit 1
    fi
}

run_game() {
    require_dependencies
    exec "$PYTHON_BIN" "$PROJECT_DIR/$1"
}

run_tests() {
    require_dependencies
    for test_file in \
        test_all_games.py \
        test_core.py \
        test_battleship_arena.py \
        test_auto_battle_logic.py \
        test_number_guessing_ai.py; do
        "$PYTHON_BIN" "$PROJECT_DIR/$test_file"
    done
}

case "${1:-}" in
    "setup")
        setup
        ;;
    "test")
        run_tests
        ;;
    "launcher"|"menu"|"l")
        run_game "game_launcher.py"
        ;;
    "snake"|"s")
        run_game "snake_game.py"
        ;;
    "guess"|"number"|"g")
        run_game "number_guessing_game.py"
        ;;
    "ascii"|"art"|"a")
        run_game "ascii_art_generator.py"
        ;;
    "battleship"|"battle"|"b")
        run_game "battleship_game.py"
        ;;
    "arena")
        run_game "battleship_arena.py"
        ;;
    ""|"help"|"--help"|"-h")
        usage
        ;;
    *)
        echo "❌ Unknown command: $1" >&2
        usage >&2
        exit 1
        ;;
esac
