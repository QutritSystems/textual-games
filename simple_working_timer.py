#!/usr/bin/env python3
"""
簡單易用的計時器
解決虛擬環境中的輸入問題
"""

import time
import threading
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.prompt import IntPrompt
from rich import box

class SimpleWorkingTimer:
    """簡單工作的計時器"""
    
    def __init__(self):
        self.console = Console()
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_duration = 0
        self.target_time = None
        self.timer_type = "stopwatch"
        
    def format_time(self, seconds: float) -> str:
        """格式化時間顯示"""
        if seconds < 0:
            seconds = 0
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def get_elapsed_time(self) -> float:
        """獲取已經過的時間"""
        if not self.start_time:
            return 0
        
        if self.paused:
            return self.paused_at - self.start_time - self.pause_duration
        else:
            return time.time() - self.start_time - self.pause_duration
    
    def get_display_time(self) -> float:
        """獲取要顯示的時間"""
        elapsed = self.get_elapsed_time()
        
        if self.timer_type in ["countdown", "pomodoro"] and self.target_time:
            return max(0, self.target_time - elapsed)
        else:
            return elapsed
    
    def show_timer_display(self):
        """顯示計時器狀態"""
        self.console.clear()
        
        # 標題
        title_text = "⏰ 簡單計時器"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 計時器顯示
        display_time = self.get_display_time()
        time_str = self.format_time(display_time)
        
        # 根據狀態設置顏色和樣式
        if self.timer_type in ["countdown", "pomodoro"]:
            if display_time <= 0:
                color = "red blink"
                status_emoji = "🔔"
                status_text = "時間到！"
            elif display_time <= 60:
                color = "yellow bold"
                status_emoji = "⚠️"
                status_text = "即將結束"
            else:
                color = "green bold"
                status_emoji = "⏰"
                status_text = "倒數中"
        else:
            color = "cyan bold"
            status_emoji = "⏱️"
            status_text = "計時中"
        
        if self.paused:
            color = "yellow"
            status_emoji = "⏸️"
            status_text = "已暫停"
        elif not self.running:
            color = "red"
            status_emoji = "⏹️"
            status_text = "準備開始"
        
        # 設置計時器標題
        if self.timer_type == "countdown":
            timer_title = "🕐 倒數計時器"
        elif self.timer_type == "pomodoro":
            timer_title = "🍅 番茄鐘 (25分鐘)"
        else:
            timer_title = "⏱️ 秒錶"
        
        # 創建顯示表格
        display_table = Table.grid()
        display_table.add_column(justify="center")
        
        display_table.add_row(f"[bold cyan]{title_text}[/]")
        display_table.add_row(f"[dim]{current_datetime}[/]")
        display_table.add_row("")
        display_table.add_row(f"[bold blue]{timer_title}[/]")
        display_table.add_row("")
        display_table.add_row(f"[{color}]{time_str}[/]")
        display_table.add_row(f"[dim]{status_emoji} {status_text}[/]")
        
        self.console.print(Panel(display_table, border_style="blue"))
        
        # 模式資訊
        mode_info = ""
        if self.timer_type == "countdown" and self.target_time:
            mode_info = f"目標時間: {int(self.target_time//60)}分鐘"
        elif self.timer_type == "pomodoro":
            mode_info = "番茄工作法 - 專注25分鐘"
        else:
            mode_info = "自由計時模式"
        
        self.console.print(f"[dim]模式: {mode_info}[/]")
        self.console.print()
        
        return display_time <= 0 and self.timer_type in ["countdown", "pomodoro"]
    
    def start_timer(self):
        """開始計時器"""
        if not self.running:
            self.start_time = time.time()
            self.pause_duration = 0
            self.running = True
            self.paused = False
        elif self.paused:
            # 恢復計時
            self.pause_duration += time.time() - self.paused_at
            self.paused = False
    
    def pause_timer(self):
        """暫停計時器"""
        if self.running and not self.paused:
            self.paused = True
            self.paused_at = time.time()
        elif self.paused:
            # 恢復
            self.pause_duration += time.time() - self.paused_at
            self.paused = False
    
    def reset_timer(self):
        """重置計時器"""
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_duration = 0
    
    def choose_mode(self):
        """選擇計時器模式"""
        self.console.clear()
        
        table = Table(title="⏰ 選擇計時器模式")
        table.add_column("選項", style="cyan", width=6)
        table.add_column("模式", style="green", width=12)
        table.add_column("說明", style="yellow")
        
        table.add_row("1", "⏱️ 秒錶", "正向計時，測量經過時間")
        table.add_row("2", "⏰ 倒數計時", "設定時間後倒數")
        table.add_row("3", "🍅 番茄鐘", "25分鐘專注工作")
        
        self.console.print(table)
        
        try:
            choice = IntPrompt.ask("請選擇模式", choices=["1", "2", "3"], default=1)
            
            if choice == 1:
                self.timer_type = "stopwatch"
                self.target_time = None
            elif choice == 2:
                minutes = IntPrompt.ask("倒數計時分鐘數", default=5)
                # 確保輸入有效範圍
                if minutes < 1:
                    minutes = 1
                    self.console.print("[yellow]輸入過小，已設為1分鐘[/]")
                elif minutes > 999:
                    minutes = 999
                    self.console.print("[yellow]輸入過大，已設為999分鐘[/]")
                self.timer_type = "countdown"
                self.target_time = minutes * 60
            elif choice == 3:
                self.timer_type = "pomodoro"
                self.target_time = 25 * 60
            
            self.reset_timer()
            return True
        except (KeyboardInterrupt, EOFError):
            return False
    
    def run_timer_session(self):
        """運行一個計時器會話"""
        self.console.print("計時器準備就緒！")
        self.console.print("[cyan]可用命令: start(開始) | pause(暫停) | reset(重置) | status(狀態) | quit(退出)[/]")
        self.console.print()
        
        while True:
            try:
                # 顯示當前狀態
                time_up = self.show_timer_display()
                
                # 如果時間到了
                if time_up and self.running:
                    self.running = False
                    self.console.print("[red bold blink]⏰ 時間到了！⏰[/]", justify="center")
                    
                    # macOS語音提醒
                    try:
                        import os
                        os.system("say '時間到了!'")
                    except:
                        pass
                    
                    self.console.print("按 Enter 繼續...")
                    input()
                    self.reset_timer()
                    continue
                
                # 獲取用戶命令
                self.console.print("[green]輸入命令：[/]", end=" ")
                cmd = input().strip().lower()
                
                if cmd in ["start", "s"]:
                    self.start_timer()
                    self.console.print("✓ 計時器已開始")
                elif cmd in ["pause", "p"]:
                    if self.running:
                        self.pause_timer()
                        if self.paused:
                            self.console.print("⏸️ 計時器已暫停")
                        else:
                            self.console.print("▶️ 計時器已恢復")
                    else:
                        self.console.print("❌ 計時器未運行")
                elif cmd in ["reset", "r"]:
                    self.reset_timer()
                    self.console.print("🔄 計時器已重置")
                elif cmd in ["status", "st"]:
                    # 狀態已經在上面顯示了
                    pass
                elif cmd in ["quit", "q", "exit"]:
                    return "quit"
                elif cmd in ["mode", "m"]:
                    return "mode"
                elif cmd == "":
                    # 空命令，只是刷新顯示
                    pass
                else:
                    self.console.print(f"❓ 未知命令: {cmd}")
                
                self.console.print()
                time.sleep(0.5)  # 短暫暫停，讓顯示更穩定
                
            except (KeyboardInterrupt, EOFError):
                return "quit"
    
    def run(self):
        """運行計時器主程式"""
        self.console.print("🚀 歡迎使用簡單計時器！")
        
        try:
            while True:
                if not self.choose_mode():
                    break
                
                result = self.run_timer_session()
                
                if result == "quit":
                    break
                # 如果是 "mode"，繼續循環選擇模式
                
        except KeyboardInterrupt:
            pass
        
        self.console.print("\n[green]感謝使用簡單計時器！[/] 👋")

def main():
    """主函數"""
    try:
        timer = SimpleWorkingTimer()
        timer.run()
    except KeyboardInterrupt:
        print("\n👋 再見！")

if __name__ == "__main__":
    main()
