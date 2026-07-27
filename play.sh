#!/bin/bash
# 🎮 Textual Games 啟動腳本
# 方便啟動遊戲的腳本

echo "🎮 Textual Games Collection"
echo "=========================="

# 檢查虛擬環境是否存在
if [ ! -d "../textual-env" ]; then
    echo "❌ 找不到 textual-env 虛擬環境"
    echo "請先運行: python3 -m venv textual-env && source textual-env/bin/activate && pip install 'textual[dev]>=0.45.0'"
    exit 1
fi

# 激活虛擬環境
source ../textual-env/bin/activate

# 如果沒有參數，顯示遊戲選單
if [ $# -eq 0 ]; then
    echo ""
echo "可用遊戲："
echo "  1. 🐍 Snake Game      - python snake_game.py"
echo "  2. 🎯 Number Guessing - python number_guessing_game.py" 
echo "  3. 🎨 ASCII Art Gen   - python ascii_art_generator.py"
echo "  4. 🚀 Game Launcher   - python game_launcher.py"
echo ""
echo "使用方法："
echo "  ./play.sh launcher    # 啟動遊戲選擇器"
echo "  ./play.sh snake      # 直接啟動貪食蛇遊戲"
echo "  ./play.sh guess      # 直接啟動猜數字遊戲"
echo "  ./play.sh ascii      # 直接啟動ASCII藝術生成器"
    echo ""
    exit 0
fi

# 根據參數啟動相對應的遊戲
case "$1" in
    "launcher"|"menu"|"l")
        echo "🚀 啟動遊戲選擇器..."
        python game_launcher.py
        ;;
    "snake"|"s")
        echo "🐍 啟動貪食蛇遊戲..."
        python snake_game.py
        ;;
    "guess"|"number"|"g")
        echo "🎯 啟動猜數字遊戲..."
        python number_guessing_game.py
        ;;
    "ascii"|"art"|"a")
        echo "🎨 啟動ASCII藝術生成器..."
        python ascii_art_generator.py
        ;;
    *)
        echo "❌ 未知的遊戲: $1"
        echo "可用選項: launcher, snake, guess, ascii"
        exit 1
        ;;
esac
