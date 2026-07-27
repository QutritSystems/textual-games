#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潛艇對決視覺效果調試腳本
"""

from battleship_game import GameBoard, CellState, Orientation, Ship

def test_board_visualization():
    print("🔍 調試潛艇對決視覺效果")
    print("=" * 50)
    
    # 創建測試棋盤
    board = GameBoard()
    print(f"✅ 創建了 {board.size}x{board.size} 棋盤")
    
    # 手動放置一艘船
    ship = Ship("測試戰艦", 3)
    success = board.place_ship(ship, 1, 1, Orientation.HORIZONTAL)
    print(f"✅ 船隻放置結果: {success}")
    
    if success:
        print(f"✅ 船隻位置: {ship.positions}")
        print("🎮 棋盤狀態:")
        
        # 顯示棋盤前3行
        for row in range(3):
            line = ""
            for col in range(5):
                state = board.grid[row][col]
                line += f"{state.value} "
            print(f"第{row}行: {line}")
    
    # 測試攻擊
    print("\n🎯 測試攻擊...")
    result = board.attack(1, 1)  # 攻擊船隻
    print(f"攻擊(1,1)結果: {result.value}")
    
    result = board.attack(0, 0)  # 攻擊空白
    print(f"攻擊(0,0)結果: {result.value}")
    
    print("\n🎮 攻擊後棋盤狀態:")
    for row in range(3):
        line = ""
        for col in range(5):
            state = board.grid[row][col]
            line += f"{state.value} "
        print(f"第{row}行: {line}")

if __name__ == "__main__":
    test_board_visualization()
