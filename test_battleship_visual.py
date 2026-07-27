#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決視覺效果測試版本
自動放置船隻，方便測試視覺效果
"""

from battleship_game import BattleshipGame, Ship, Orientation
import asyncio

class TestBattleshipGame(BattleshipGame):
    """測試版本 - 自動放置船隻"""
    
    def on_mount(self):
        """應用啟動時自動放置船隻"""
        super().on_mount()
        # 等待 UI 完全初始化後再放置船隻
        self.set_timer(0.5, self.auto_setup_test_ships)
    
    def auto_setup_test_ships(self):
        """自動設置測試船隻"""
        print("🔧 自動放置測試船隻...")
        
        # 為玩家放置幾艘船用於測試
        test_ships = [
            ("測試戰艦", 3, 1, 1, Orientation.HORIZONTAL),
            ("測試巡洋艦", 2, 3, 3, Orientation.VERTICAL),
            ("測試潛艇", 1, 5, 5, Orientation.HORIZONTAL)
        ]
        
        for ship_name, size, row, col, orientation in test_ships:
            ship = Ship(ship_name, size)
            if self.player_board.place_ship(ship, row, col, orientation):
                print(f"✅ 放置了 {ship_name} 在 ({row},{col})")
            else:
                print(f"❌ 無法放置 {ship_name}")
        
        # 更新玩家網格顯示
        if self.player_grid:
            self.player_grid.update_grid()
        
        # 更新AI網格顯示（會隱藏船隻）
        if self.ai_grid:
            self.ai_grid.update_grid()
        
        self.update_status("✅ 測試船隻已放置！點擊敵方戰場開始攻擊")
        
        # 直接進入戰鬥模式
        self.game_phase = self.game_phase.BATTLE
        
        # 啟用AI網格點擊
        if self.ai_grid:
            for row in range(self.ai_grid.board.size):
                for col in range(self.ai_grid.board.size):
                    self.ai_grid.cells[row][col].clickable = True

def main():
    """運行測試版本"""
    print("🚢 啟動潛艇對決視覺效果測試版本...")
    print("📝 特色:")
    print("  - 自動放置測試船隻")
    print("  - 直接進入戰鬥模式")
    print("  - 方便測試視覺效果")
    print()
    
    app = TestBattleshipGame()
    app.run()

if __name__ == "__main__":
    main()
