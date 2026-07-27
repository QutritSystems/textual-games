#!/usr/bin/env python3
"""
簡單的 Rich 計時器
不依賴外部按鍵庫，使用輸入命令控制
"""

import time
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

class SimpleRichTimer:
    """簡單的 Rich 計時器"""
    
    def __init__(self):
        self.console = Console()
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_duration = 0
        self.target_time = None
        self.timer_type = "stopwatch"
        self.should_exit = False
        
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
            Layout(name="controls", size=6),
            Layout(name="status", size=3)
        )
        
        # 標題
        title_text = "⏰ Rich 計時器"
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
        controls.add_column("命令", style="cyan", width=8)
        controls.add_column("功能", style="green")
        
        controls.add_row("start", "開始計時器")
        controls.add_row("pause", "暫停/繼續")
        controls.add_row("reset", "重置計時器")
        controls.add_row("mode", "切換模式")
        controls.add_row("quit", "退出程式")
        
        layout["controls"].update(Panel(
            controls,
            title="📖 命令說明",
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
                minutes = IntPrompt.ask("倒數計時分鐘數", default=5, min=1, max=999)
                self.timer_type = "countdown"
                self.target_time = minutes * 60
            elif choice == 3:
                self.timer_type = "pomodoro"
                self.target_time = 25 * 60
            
            self.reset_timer()
        except (KeyboardInterrupt, EOFError):
            pass
    
    def handle_input(self):
        """處理用戶輸入的線程函數"""
        while not self.should_exit:
            try:
                cmd = input().strip().lower()
                
                if cmd in ["start", "s"]:
                    self.start_timer()
                elif cmd in ["pause", "p"]:
                    self.pause_timer()
                elif cmd in ["reset", "r"]:
                    self.reset_timer()
                elif cmd in ["mode", "m"]:
                    self.should_exit = True
                    break
                elif cmd in ["quit", "q", "exit"]:
                    self.should_exit = True
                    break
                    
            except EOFError:
                self.should_exit = True
                break
            except KeyboardInterrupt:
                self.should_exit = True
                break
    
    def run(self):
        """運行計時器"""
        while True:
            self.choose_mode()
            if self.should_exit:
                break
                
            self.should_exit = False
            
            # 啟動輸入處理線程
            input_thread = threading.Thread(target=self.handle_input, daemon=True)
            input_thread.start()
            
            try:
                with Live(self.create_display(), refresh_per_second=2, screen=True) as live:
                    self.console.print("[dim]輸入命令開始使用（如: start, pause, reset, mode, quit）[/]")
                    
                    while not self.should_exit:
                        live.update(self.create_display())
                        
                        # 檢查倒數計時是否結束
                        if (self.timer_type in ["countdown", "pomodoro"] and 
                            self.running and not self.paused and 
                            self.get_display_time() <= 0):
                            
                            # 時間到了
                            self.running = False
                            live.update(self.create_display())
                            
                            # macOS 語音提醒
                            try:
                                import os
                                os.system("say '時間到了!'")
                            except:
                                pass
                            
                            self.console.print("\n[red bold blink]⏰ 時間到了！⏰[/]", justify="center")
                            input("按 Enter 繼續...")
                            self.reset_timer()
                        
                        time.sleep(0.5)
                        
            except KeyboardInterrupt:
                self.should_exit = True
                break
            
            if not self.should_exit:
                # 如果是模式切換，繼續循環
                continue
            else:
                break
        
        self.console.print("\n[green]感謝使用 Rich 計時器！[/] 👋")

def main():
    """主函數"""
    print("🚀 啟動簡單 Rich 計時器...")
    
    try:
        timer = SimpleRichTimer()
        timer.run()
    except KeyboardInterrupt:
        print("\n👋 再見！")

if __name__ == "__main__":
    main()
