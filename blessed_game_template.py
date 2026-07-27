#!/usr/bin/env python3
"""
Blessed 遊戲模板
展示如何使用 Blessed 創建終端遊戲
"""

import time
import random
from blessed import Terminal

class SimpleSnakeGame:
    """使用 Blessed 的簡單貪食蛇遊戲"""
    
    def __init__(self):
        self.term = Terminal()
        self.width = min(80, self.term.width - 2)
        self.height = min(20, self.term.height - 4)
        self.snake = [(10, 10)]
        self.direction = (0, 1)
        self.food = self.generate_food()
        self.score = 0
        self.running = True
        
    def generate_food(self):
        """生成食物位置"""
        while True:
            food = (random.randint(1, self.width-2), random.randint(1, self.height-2))
            if food not in self.snake:
                return food
    
    def draw_border(self):
        """繪制邊框"""
        # 頂部邊框
        print(self.term.move(0, 0) + '┌' + '─' * (self.width-2) + '┐')
        
        # 側邊框
        for y in range(1, self.height-1):
            print(self.term.move(y, 0) + '│')
            print(self.term.move(y, self.width-1) + '│')
            
        # 底部邊框
        print(self.term.move(self.height-1, 0) + '└' + '─' * (self.width-2) + '┘')
    
    def draw_snake(self):
        """繪制蛇"""
        # 清除舊的蛇身
        for x, y in self.snake:
            if 0 <= x < self.width and 0 <= y < self.height:
                print(self.term.move(y, x) + ' ')
        
        # 繪制新的蛇身
        for i, (x, y) in enumerate(self.snake):
            if 0 <= x < self.width and 0 <= y < self.height:
                if i == 0:  # 蛇頭
                    print(self.term.move(y, x) + self.term.bold_green('●'))
                else:  # 蛇身
                    print(self.term.move(y, x) + self.term.green('○'))
    
    def draw_food(self):
        """繪制食物"""
        x, y = self.food
        print(self.term.move(y, x) + self.term.bold_red('🍎'))
    
    def draw_score(self):
        """繪制分數"""
        print(self.term.move(self.height + 1, 0) + f"分數: {self.score}")
        print(self.term.move(self.height + 2, 0) + "按 q 退出，WASD 控制方向")
    
    def update(self):
        """更新遊戲狀態"""
        if not self.running:
            return
            
        # 移動蛇頭
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # 檢查撞牆
        if (new_head[0] <= 0 or new_head[0] >= self.width-1 or 
            new_head[1] <= 0 or new_head[1] >= self.height-1):
            self.running = False
            return
            
        # 檢查撞自己
        if new_head in self.snake:
            self.running = False
            return
        
        # 移動蛇
        self.snake.insert(0, new_head)
        
        # 檢查吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def handle_input(self):
        """處理輸入"""
        key = self.term.inkey(timeout=0)
        
        if key:
            if key.lower() == 'q':
                self.running = False
            elif key.lower() == 'w' and self.direction != (0, 1):
                self.direction = (0, -1)
            elif key.lower() == 's' and self.direction != (0, -1):
                self.direction = (0, 1)
            elif key.lower() == 'a' and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif key.lower() == 'd' and self.direction != (-1, 0):
                self.direction = (1, 0)
    
    def run(self):
        """運行遊戲"""
        with self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.clear())
            
            while self.running:
                # 清屏
                print(self.term.move(0, 0))
                
                # 繪制遊戲元素
                self.draw_border()
                self.draw_snake()
                self.draw_food()
                self.draw_score()
                
                # 處理輸入
                self.handle_input()
                
                # 更新遊戲狀態
                self.update()
                
                # 控制遊戲速度
                time.sleep(0.15)
            
            # 遊戲結束
            print(self.term.move(self.height // 2, self.width // 2 - 10))
            print(self.term.bold_red("遊戲結束！"))
            print(self.term.move(self.height // 2 + 1, self.width // 2 - 10))
            print(f"最終分數: {self.score}")
            print(self.term.move(self.height // 2 + 2, self.width // 2 - 10))
            print("按任意鍵退出...")
            self.term.inkey()

class MenuSystem:
    """使用 Blessed 的菜單系統示例"""
    
    def __init__(self):
        self.term = Terminal()
        
    def show_menu(self):
        """顯示主菜單"""
        options = [
            "🐍 貪食蛇遊戲",
            "🎯 其他遊戲 (待開發)",
            "⚙️  設定",
            "❌ 退出"
        ]
        
        selected = 0
        
        with self.term.cbreak():
            while True:
                print(self.term.clear())
                print(self.term.move(2, 0) + self.term.bold_cyan("🎮 終端遊戲中心"))
                print(self.term.move(3, 0) + "─" * 40)
                
                for i, option in enumerate(options):
                    y_pos = 5 + i * 2
                    if i == selected:
                        print(self.term.move(y_pos, 2) + 
                              self.term.reverse(f"→ {option} ←"))
                    else:
                        print(self.term.move(y_pos, 2) + f"  {option}")
                
                print(self.term.move(15, 0) + "使用 ↑↓ 選擇，Enter 確認")
                
                key = self.term.inkey()
                
                if key.code == self.term.KEY_UP:
                    selected = (selected - 1) % len(options)
                elif key.code == self.term.KEY_DOWN:
                    selected = (selected + 1) % len(options)
                elif key.code == self.term.KEY_ENTER:
                    return selected
                elif key.lower() == 'q':
                    return 3  # 退出

def main():
    """主函數"""
    try:
        # 檢查終端大小
        term = Terminal()
        if term.width < 80 or term.height < 25:
            print("終端太小！請調整到至少 80x25")
            return
        
        menu = MenuSystem()
        
        while True:
            choice = menu.show_menu()
            
            if choice == 0:  # 貪食蛇遊戲
                game = SimpleSnakeGame()
                game.run()
            elif choice == 1:  # 其他遊戲
                print(term.clear())
                print("其他遊戲正在開發中...")
                print("按任意鍵返回菜單")
                term.inkey()
            elif choice == 2:  # 設定
                print(term.clear())
                print("設定功能正在開發中...")
                print("按任意鍵返回菜單")
                term.inkey()
            elif choice == 3:  # 退出
                print(term.clear())
                print("感謝遊玩！👋")
                break
                
    except KeyboardInterrupt:
        print("\n再見！")

if __name__ == "__main__":
    main()
