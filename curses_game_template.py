#!/usr/bin/env python3
"""
Curses 遊戲模板
展示如何使用內建 curses 創建終端遊戲
"""

import curses
import random
import time

class TetrisGame:
    """使用 Curses 的簡化俄羅斯方塊"""
    
    SHAPES = [
        [['....', '####', '....', '....']],  # I
        [['..##', '.##.', '....', '....']],  # S
        [['.##.', '##..', '....', '....']],  # Z
        [['....', '.##.', '.##.', '....']],  # O
        [['....', '.#..', '###.', '....']],  # T
        [['....', '..#.', '###.', '....']],  # L
        [['....', '.#..', '##..', '....']],  # J (簡化版)
    ]
    
    COLORS = [1, 2, 3, 4, 5, 6, 7]
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height = 20
        self.width = 10
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.current_piece = self.new_piece()
        self.game_over = False
        
        # 設置顏色
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    def new_piece(self):
        """創建新方塊"""
        shape_idx = random.randint(0, len(self.SHAPES) - 1)
        return {
            'shape': self.SHAPES[shape_idx][0],
            'x': self.width // 2 - 2,
            'y': 0,
            'color': self.COLORS[shape_idx]
        }
    
    def valid_position(self, piece, dx=0, dy=0):
        """檢查位置是否有效"""
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height or
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True
    
    def place_piece(self, piece):
        """放置方塊"""
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_x = piece['x'] + x
                    board_y = piece['y'] + y
                    if board_y >= 0:
                        self.board[board_y][board_x] = piece['color']
    
    def clear_lines(self):
        """清除滿行"""
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(self.board[y]):
                del self.board[y]
                self.board.insert(0, [0] * self.width)
                lines_cleared += 1
            else:
                y -= 1
        
        self.score += lines_cleared * 100
    
    def draw(self):
        """繪制遊戲"""
        self.stdscr.clear()
        
        # 繪制邊框
        for y in range(self.height + 2):
            self.stdscr.addch(y, 0, '|')
            self.stdscr.addch(y, self.width * 2 + 1, '|')
        
        for x in range(self.width * 2 + 2):
            self.stdscr.addch(self.height + 1, x, '-')
        
        # 繪制已放置的方塊
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    color = self.board[y][x]
                    self.stdscr.addstr(y + 1, x * 2 + 1, '██', 
                                     curses.color_pair(color))
        
        # 繪制當前方塊
        if not self.game_over:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell == '#':
                        screen_x = (self.current_piece['x'] + x) * 2 + 1
                        screen_y = self.current_piece['y'] + y + 1
                        if screen_y > 0 and screen_x > 0:
                            try:
                                self.stdscr.addstr(screen_y, screen_x, '██', 
                                                 curses.color_pair(self.current_piece['color']))
                            except curses.error:
                                pass
        
        # 顯示分數和控制說明
        info_x = self.width * 2 + 5
        self.stdscr.addstr(1, info_x, f"分數: {self.score}")
        self.stdscr.addstr(3, info_x, "控制:")
        self.stdscr.addstr(4, info_x, "A/D - 左右移動")
        self.stdscr.addstr(5, info_x, "S - 快速下降")
        self.stdscr.addstr(6, info_x, "W - 旋轉 (暫未實現)")
        self.stdscr.addstr(7, info_x, "Q - 退出")
        
        if self.game_over:
            msg = "遊戲結束！按 Q 退出"
            self.stdscr.addstr(self.height // 2, 
                             (self.width * 2 - len(msg)) // 2 + 1, 
                             msg, curses.color_pair(1) | curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def update(self):
        """更新遊戲狀態"""
        if self.game_over:
            return
        
        # 嘗試向下移動
        if self.valid_position(self.current_piece, dy=1):
            self.current_piece['y'] += 1
        else:
            # 放置方塊
            self.place_piece(self.current_piece)
            self.clear_lines()
            
            # 生成新方塊
            self.current_piece = self.new_piece()
            
            # 檢查遊戲結束
            if not self.valid_position(self.current_piece):
                self.game_over = True
    
    def handle_input(self):
        """處理輸入"""
        self.stdscr.timeout(100)  # 100ms 超時
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            return False
        elif key == ord('a') or key == ord('A'):
            if self.valid_position(self.current_piece, dx=-1):
                self.current_piece['x'] -= 1
        elif key == ord('d') or key == ord('D'):
            if self.valid_position(self.current_piece, dx=1):
                self.current_piece['x'] += 1
        elif key == ord('s') or key == ord('S'):
            if self.valid_position(self.current_piece, dy=1):
                self.current_piece['y'] += 1
        
        return True
    
    def run(self):
        """運行遊戲"""
        last_drop = time.time()
        drop_interval = 1.0  # 1秒下降一次
        
        while True:
            # 繪制
            self.draw()
            
            # 處理輸入
            if not self.handle_input():
                break
            
            # 自動下降
            current_time = time.time()
            if current_time - last_drop >= drop_interval:
                self.update()
                last_drop = current_time

class Menu:
    """Curses 菜單系統"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.options = [
            "🎮 俄羅斯方塊",
            "🎲 其他遊戲",
            "❌ 退出"
        ]
        self.selected = 0
    
    def draw(self):
        """繪制菜單"""
        self.stdscr.clear()
        
        height, width = self.stdscr.getmaxyx()
        
        # 標題
        title = "🎮 Curses 遊戲中心"
        x = (width - len(title)) // 2
        self.stdscr.addstr(3, x, title, curses.A_BOLD)
        
        # 分隔線
        separator = "─" * 40
        x = (width - len(separator)) // 2
        self.stdscr.addstr(4, x, separator)
        
        # 選項
        for i, option in enumerate(self.options):
            y = 6 + i * 2
            x = (width - len(option)) // 2
            
            if i == self.selected:
                self.stdscr.addstr(y, x, f"→ {option} ←", curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, f"  {option}  ")
        
        # 說明
        help_text = "使用 ↑↓ 選擇，Enter 確認"
        x = (width - len(help_text)) // 2
        self.stdscr.addstr(height - 3, x, help_text)
        
        self.stdscr.refresh()
    
    def handle_input(self):
        """處理輸入"""
        key = self.stdscr.getch()
        
        if key == curses.KEY_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif key == curses.KEY_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == ord('\n') or key == ord('\r'):
            return self.selected
        elif key == ord('q') or key == ord('Q'):
            return 2  # 退出
        
        return -1
    
    def run(self):
        """運行菜單"""
        while True:
            self.draw()
            choice = self.handle_input()
            if choice != -1:
                return choice

def main(stdscr):
    """主函數"""
    # 設置 curses
    curses.curs_set(0)  # 隱藏光標
    stdscr.keypad(True)  # 啟用特殊鍵
    
    # 檢查終端大小
    height, width = stdscr.getmaxyx()
    if height < 25 or width < 50:
        stdscr.addstr(0, 0, "終端太小！請調整到至少 50x25")
        stdscr.getch()
        return
    
    menu = Menu(stdscr)
    
    while True:
        choice = menu.run()
        
        if choice == 0:  # 俄羅斯方塊
            game = TetrisGame(stdscr)
            game.run()
        elif choice == 1:  # 其他遊戲
            stdscr.clear()
            stdscr.addstr(10, 10, "其他遊戲正在開發中...")
            stdscr.addstr(11, 10, "按任意鍵返回菜單")
            stdscr.getch()
        elif choice == 2:  # 退出
            stdscr.clear()
            stdscr.addstr(10, 10, "感謝遊玩！")
            stdscr.refresh()
            time.sleep(1)
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("再見！")
