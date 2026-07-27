#!/usr/bin/env python3
"""
修復的 Rich 計時器
解決輸入問題，使用更好的終端處理
"""

import time
import sys
import select
import termios
import tty
import threading
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.prompt import IntPrompt, Prompt
from rich import box

class FixedRichTimer:
    """修復的 Rich 計時器"""
    
    def __init__(self):
        self.console = Console()
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_duration = 0
        self.target_time = None
        self.timer_type = "stopwatch"
        self.should_exit = False
        self.old_settings = None
        
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
    
    def create_display(self) -> Layout:
        """創建顯示佈局"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="timer", size=8),
            Layout(name="controls", size=8),
            Layout(name="status", size=3)
        )
        
        # 標題
        title_text = "⏰ 修復版計時器"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header_table = Table.grid()
        header_table.add_column(justify="center")
        header_table.add_row(f"[bold cyan]{title_text}[/]")
        header_table.add_row(f"[dim]{current_datetime}[/]")
        
        layout["header"].update(Panel(header_table, border_style="blue"))
        
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
            status_text = "已停止"
        
        # 大字體時間
        timer_display = Text(time_str, style=f"{color}")
        timer_content = Align.center(Text.assemble(
            timer_display, "\n",
            Text(f"{status_emoji} {status_text}", style="dim")
        ))
        
        # 設置計時器標題
        if self.timer_type == "countdown":
            timer_title = "🕐 倒數計時器"
        elif self.timer_type == "pomodoro":
            timer_title = "🍅 番茄鐘 (25分鐘)"
        else:
            timer_title = "⏱️ 秒錶"
        
        layout["timer"].update(Panel(
            timer_content, 
            title=timer_title,
            border_style="bright_blue",
            box=box.DOUBLE
        ))
        
        # 控制說明
        controls = Table(box=box.ROUNDED)
        controls.add_column("按鍵", style="cyan", width=8)
        controls.add_column("功能", style="green")
        
        controls.add_row("SPACE", "開始/暫停")
        controls.add_row("r", "重置計時器")
        controls.add_row("m", "切換模式")
        controls.add_row("q", "退出程式")
        controls.add_row("", "")
        controls.add_row("[dim]注意[/]", "[dim]請按鍵後稍等更新[/]")
        
        layout["controls"].update(Panel(
            controls,
            title="📖 按鍵說明",
            border_style="magenta"
        ))
        
        # 狀態欄
        mode_info = ""
        if self.timer_type == "countdown" and self.target_time:
            mode_info = f"目標: {int(self.target_time//60)}分鐘"
        elif self.timer_type == "pomodoro":
            mode_info = "番茄工作法 - 專注25分鐘"
        else:
            mode_info = "自由計時模式"
        
        layout["status"].update(Panel(
            f"[dim]{mode_info}[/]",
            border_style="dim"
        ))
        
        return layout
    
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
    
    def setup_terminal(self):
        """設置終端為原始模式"""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
    
    def restore_terminal(self):
        """恢復終端設置"""
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def get_char(self):
        """非阻塞獲取字符"""
        if sys.stdin.isatty() and select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None
    
    def handle_key(self, key):
        """處理按鍵"""
        if key == ' ':  # 空格鍵：開始/暫停
            if not self.running:
                self.start_timer()
            else:
                self.pause_timer()
        elif key.lower() == 'r':  # r：重置
            self.reset_timer()
        elif key.lower() == 'm':  # m：切換模式
            self.should_exit = True
            return 'mode'
        elif key.lower() == 'q':  # q：退出
            self.should_exit = True
            return 'quit'
        elif key == '\x03':  # Ctrl+C
            self.should_exit = True
            return 'quit'
        
        return None
    
    def run_timer_mode(self):
        """運行計時器模式"""
        self.should_exit = False
        self.setup_terminal()
        
        try:
            with Live(self.create_display(), refresh_per_second=2, screen=False) as live:
                self.console.print("\n[dim]使用按鍵控制計時器（空格：開始/暫停，r：重置，m：模式，q：退出）[/]")
                
                while not self.should_exit:
                    # 更新顯示
                    live.update(self.create_display())
                    
                    # 檢查按鍵輸入
                    key = self.get_char()
                    if key:
                        result = self.handle_key(key)
                        if result in ['mode', 'quit']:
                            break
                    
                    # 檢查倒數計時是否結束
                    if (self.timer_type in ["countdown", "pomodoro"] and 
                        self.running and not self.paused and 
                        self.get_display_time() <= 0):
                        
                        # 時間到了
                        self.running = False
                        live.update(self.create_display())
                        
                        # 語音提醒 (macOS)
                        try:
                            import os
                            os.system("say '時間到了!'")
                        except:
                            pass
                        
                        self.console.print("\n[red bold blink]⏰ 時間到了！⏰[/]", justify="center")
                        self.console.print("[dim]按任意鍵繼續...[/]")
                        
                        # 等待任意鍵
                        while not self.get_char():
                            time.sleep(0.1)
                        
                        self.reset_timer()
                    
                    time.sleep(0.1)  # 減少CPU使用
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.restore_terminal()
        
        return 'mode' if not self.should_exit else 'quit'
    
    def run(self):
        """運行計時器"""
        self.console.print("🚀 啟動修復版計時器...")
        
        try:
            while True:
                if not self.choose_mode():
                    break
                    
                result = self.run_timer_mode()
                
                if result == 'quit':
                    break
                # 如果是 'mode'，繼續循環選擇模式
                
        except KeyboardInterrupt:
            pass
        finally:
            self.restore_terminal()
            self.console.print("\n[green]感謝使用修復版計時器！[/] 👋")

def main():
    """主函數"""
    try:
        timer = FixedRichTimer()
        timer.run()
    except KeyboardInterrupt:
        print("\n👋 再見！")

if __name__ == "__main__":
    main()
