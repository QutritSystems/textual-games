#!/bin/bash

echo "=== 終端環境檢查 ==="
echo "終端程式: $TERM_PROGRAM"
echo "TERM 變數: $TERM"
echo "色彩支援: $(tput colors)"
echo "COLORTERM: $COLORTERM"
echo ""

echo "=== 基本功能測試 ==="
echo "清屏測試..."
clear
echo "這行文字應該在螢幕頂部"
echo ""

echo "=== 色彩測試 ==="
echo -e "\033[31m紅色文字\033[0m"
echo -e "\033[32m綠色文字\033[0m"
echo -e "\033[34m藍色文字\033[0m"
echo ""

echo "=== 字符測試 ==="
echo "Unicode: 🔥 ⭐ 🎯"
echo "ASCII: S X o # ~"
echo "Box: ┌─┐│ │└─┘"
echo ""

echo "=== Python Textual 測試 ==="
python -c "
try:
    from textual.app import App
    from textual.widgets import Static
    
    class QuickTest(App):
        def compose(self):
            yield Static('成功!')
        def on_mount(self):
            print('Textual 初始化成功!')
            self.exit()
    
    app = QuickTest()
    print('開始 Textual 測試...')
    app.run()
    print('Textual 測試完成')
    
except Exception as e:
    print(f'Textual 錯誤: {e}')
    import traceback
    traceback.print_exc()
"
