#!/usr/bin/env python3
"""
檢查 Game Launcher 顯示的遊戲選項
"""

from game_launcher import GameLauncher
import sys

def main():
    print("🔍 Game Launcher 顯示檢查")
    print("=" * 35)
    
    try:
        app = GameLauncher()
        
        # 檢查 compose 方法中的遊戲
        import inspect
        source = inspect.getsource(app.compose)
        
        games_found = []
        
        if "🐍 Snake Game" in source:
            games_found.append("🐍 Snake Game (貪食蛇)")
        
        if "🎯 Number Guessing" in source:
            games_found.append("🎯 Number Guessing (猜數字)")
            
        if "🚀 More Games" in source:
            games_found.append("🚀 More Games (敬請期待)")
        
        print(f"📊 找到的遊戲選項: {len(games_found)} 個")
        for i, game in enumerate(games_found, 1):
            print(f"   {i}. {game}")
        
        print()
        print("🎮 遊戲按鈕檢查:")
        
        buttons_found = []
        if 'id="snake"' in source:
            buttons_found.append("Play Snake 按鈕")
        if 'id="guessing"' in source:
            buttons_found.append("Play Guessing 按鈕") 
        if 'id="coming-soon"' in source:
            buttons_found.append("Coming Soon 按鈕")
            
        for button in buttons_found:
            print(f"   ✅ {button}")
        
        print()
        print("📏 佈局設定檢查:")
        css = app.CSS
        if "max-height: 90vh" in css:
            print("   ✅ 使用響應式高度 (max-height: 90vh)")
        if "width: 80" in css:
            print("   ✅ 寬度設為 80 提供足夠空間")
        if "height: auto" in css:
            print("   ✅ 卡片高度自動調整")
        
        print()
        if len(games_found) >= 2:
            print("🎉 遊戲選擇器應該正常顯示所有遊戲！")
            print()
            print("💡 如果在終端中只看到一個遊戲，請嘗試：")
            print("   1. 調整終端窗口大小 (拉高一點)")
            print("   2. 使用滾輪或方向鍵上下滾動")
            print("   3. 確保終端支持豐富的文字顯示")
        else:
            print("⚠️  遊戲選項數量不足，請檢查代碼")
        
        return 0
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
