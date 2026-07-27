#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決調試版本 - 寫入日誌文件
"""

from battleship_game import *
import datetime

class LoggedBattleshipGame(BattleshipGame):
    """帶日誌的潛艇對決遊戲"""
    
    def __init__(self):
        super().__init__()
        self.log_file = open("battleship_debug.log", "w", encoding="utf-8")
        self.debug_log("🚀 遊戲初始化開始")
    
    def debug_log(self, message):
        """寫入日誌"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_file.write(f"[{timestamp}] {message}\n")
        self.log_file.flush()
    
    def on_mount(self):
        """應用啟動時的初始化"""
        self.debug_log("📱 on_mount 被調用")
        super().on_mount()
        
        # 檢查網格是否正確初始化
        self.debug_log(f"🔍 player_grid 存在: {self.player_grid is not None}")
        self.debug_log(f"🔍 ai_grid 存在: {self.ai_grid is not None}")
        
        if self.player_grid:
            self.debug_log(f"🔍 player_grid.cells 長度: {len(self.player_grid.cells)}")
            if self.player_grid.cells:
                self.debug_log(f"🔍 player_grid.cells[0] 長度: {len(self.player_grid.cells[0])}")
        
        # 延遲後放置測試船隻
        self.set_timer(1.0, self.place_test_ship)
    
    def place_test_ship(self):
        """放置測試船隻"""
        self.debug_log("🚢 開始放置測試船隻")
        
        # 創建測試船隻
        test_ship = Ship("測試船", 3)
        success = self.player_board.place_ship(test_ship, 2, 2, Orientation.HORIZONTAL)
        
        self.debug_log(f"✅ 船隻放置結果: {success}")
        if success:
            self.debug_log(f"🎯 船隻位置: {test_ship.positions}")
            
            # 檢查棋盤狀態
            for row in range(5):
                line = ""
                for col in range(5):
                    state = self.player_board.grid[row][col]
                    line += f"{state.value} "
                self.debug_log(f"棋盤第{row}行: {line}")
            
            # 更新網格
            self.debug_log("🔄 準備更新玩家網格")
            if self.player_grid and self.player_grid.cells:
                self.debug_log("🔄 調用 player_grid.update_grid()")
                self.player_grid.update_grid()
                
                # 檢查網格單元狀態
                for row in range(3):
                    for col in range(5):
                        if row < len(self.player_grid.cells) and col < len(self.player_grid.cells[row]):
                            cell = self.player_grid.cells[row][col]
                            self.debug_log(f"格子({row},{col})狀態: {cell.state.name} = {cell.state.value}")
            else:
                self.debug_log("❌ 無法更新網格：cells 不存在")
        
        self.update_status("🔧 測試船隻已放置，檢查日誌檔案")
    
    def exit(self):
        """退出時關閉日誌檔案"""
        self.debug_log("👋 遊戲結束")
        if hasattr(self, 'log_file'):
            self.log_file.close()
        super().exit()

def main():
    """運行日誌版本"""
    print("🔍 啟動帶日誌的調試版本...")
    print("📝 調試信息將寫入 battleship_debug.log")
    print("按 Q 退出遊戲")
    
    app = LoggedBattleshipGame()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n遊戲被中斷")
    finally:
        if hasattr(app, 'log_file'):
            app.log_file.close()

if __name__ == "__main__":
    main()
