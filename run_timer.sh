#!/bin/bash
# 修復虛擬環境輸入問題的運行腳本

echo "🚀 準備運行計時器..."

# 設置終端環境
export TERM=${TERM:-xterm-256color}
export PYTHONIOENCODING=utf-8
export LC_ALL=${LC_ALL:-en_US.UTF-8}

# 重置終端設定
echo "🔧 重置終端設定..."
stty sane 2>/dev/null || true

# 檢查虛擬環境
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  虛擬環境未啟動，正在啟動..."
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        echo "✅ 虛擬環境已啟動: $VIRTUAL_ENV"
    else
        echo "❌ 找不到虛擬環境: venv/bin/activate"
        exit 1
    fi
else
    echo "✅ 虛擬環境已啟動: $VIRTUAL_ENV"
fi

# 檢查 Python 和 rich
echo "🔍 檢查依賴..."
python -c "import rich; print('✅ Rich 已安裝')" 2>/dev/null || {
    echo "❌ Rich 未安裝，正在安裝..."
    pip install rich
}

echo "🎯 選擇要運行的程式:"
echo "📱 計時器系列:"
echo "1. 簡單工作計時器 (推薦)"
echo "2. 修復版計時器"
echo "3. 原始計時器"
echo "4. 終端診斷工具"
echo ""
echo "🎮 遊戲系列:"
echo "5. Blessed 遊戲模板 (貪食蛇)"
echo "6. Curses 遊戲模板 (俄羅斯方塊)"

read -p "請選擇 [1-6]: " choice

case $choice in
    1)
        echo "🚀 啟動簡單工作計時器..."
        python simple_working_timer.py
        ;;
    2)
        echo "🚀 啟動修復版計時器..."
        python fixed_rich_timer.py
        ;;
    3)
        echo "🚀 啟動原始計時器..."
        python simple_rich_timer.py
        ;;
    4)
        echo "🚀 啟動終端診斷工具..."
        python reset_terminal.py
        ;;
    5)
        echo "🚀 啟動 Blessed 遊戲模板..."
        # 檢查 blessed 是否安裝
        python -c "import blessed" 2>/dev/null || {
            echo "📦 安裝 blessed..."
            pip install blessed
        }
        python blessed_game_template.py
        ;;
    6)
        echo "🚀 啟動 Curses 遊戲模板..."
        python curses_game_template.py
        ;;
    *)
        echo "❌ 無效選擇"
        exit 1
        ;;
esac

# 程式結束後重置終端
echo "🔧 程式結束，重置終端..."
stty sane 2>/dev/null || true
echo "✅ 完成"
