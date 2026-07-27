#!/usr/bin/env python3
"""
Rich 計時器應用
支援倒數計時器、秒錶、番茄鐘等多種功能
"""

import time
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich import box
import keyboard

class RichTimer:
    """Rich 計時器類別"""
    
    def __init__(self):
        self.console = Console()
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        self.target_time = None
        self.timer_type = "stopwatch"
        
    def create_layout(self) -> Layout:
        """創建計時器佈局"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="controls", size=3)
        )
        
        return layout
    
    def format_time(self, seconds: float) -> str:
        """格式化時間顯示"""
        if seconds < 0:
            seconds = 0
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 100)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}.{milliseconds:02d}"
    
    def get_current_time(self) -> float:
        """獲取當前計時時間"""
        if not self.running:
            return 0
        
        current = time.time()
        elapsed = current - self.start_time - self.pause_time
        
        if self.timer_type == "countdown" and self.target_time:
            return max(0, self.target_time - elapsed)
        else:
            return elapsed
    
    def create_timer_display(self) -> Panel:
        """創建計時器顯示面板"""
        current_time = self.get_current_time()
        time_text = self.format_time(current_time)
        
        # 根據計時器類型設置顏色
        if self.timer_type == "countdown":
            if current_time <= 0:
                color = "red blink"
                status = "⏰ 時間到！"
            elif current_time <= 60:
                color = "yellow"
                status = "⚠️  即將結束"
            else:
                color = "green"
                status = "⏰ 倒數中..."
        else:
            color = "cyan"
            status = "⏱️  計時中..." if self.running else "⏸️  已暫停"
        
        # 創建大字體時間顯示
        time_display = Text(time_text, style=f"bold {color}")
        time_display.stylize("bold", 0, len(time_text))
        
        # 狀態文字
        if self.paused and self.running:
            status = "⏸️  已暫停"
            color = "yellow"
        elif not self.running:
            status = "⏹️  已停止"
            color = "red"
        
        status_text = Text(status, style=color)
        
        # 組合顯示內容
        content = Align.center(
            Text.assemble(
                time_display, "\n\n",
                status_text
            )
        )
        
        # 設置面板標題
        if self.timer_type == "countdown":
            title = "🕐 倒數計時器"
        elif self.timer_type == "pomodoro":
            title = "🍅 番茄鐘"
        else:
            title = "⏱️ 秒錶"
        
        return Panel(
            content,
            title=title,
            border_style="bright_blue",
            box=box.DOUBLE
        )
    
    def create_controls_panel(self) -> Panel:
        """創建控制面板"""
        controls = Table.grid(padding=1)
        controls.add_column(justify="center")
        
        if not self.running:
            controls.add_row("[green]SPACE[/] 開始")
        else:
            if self.paused:
                controls.add_row("[green]SPACE[/] 繼續")
            else:
                controls.add_row("[yellow]SPACE[/] 暫停")
        
        controls.add_row("[red]R[/] 重置")
        controls.add_row("[blue]M[/] 模式選擇")
        controls.add_row("[red]Q[/] 退出")
        
        return Panel(
            Align.center(controls),
            title="⌨️  控制鍵",
            border_style="bright_magenta"
        )
    
    def create_info_panel(self) -> Panel:
        """創建資訊面板"""
        info = Table.grid(padding=1)
        info.add_column(justify="left")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        info.add_row(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
        info.add_row(f"🕐 {current_time}")
        
        if self.timer_type == "countdown" and self.target_time:
            target_minutes = int(self.target_time // 60)
            info.add_row(f"🎯 目標: {target_minutes}分鐘")
        elif self.timer_type == "pomodoro":
            info.add_row("🍅 番茄鐘: 25分鐘工作")
        
        return Panel(
            info,
            title="ℹ️  資訊",
            border_style="bright_green"
        )
    
    def start_timer(self):
        """開始計時器"""
        if not self.running:
            self.start_time = time.time()
            self.pause_time = 0
        elif self.paused:
            # 恢復計時
            self.pause_time += time.time() - self.paused_at
        
        self.running = True
        self.paused = False
    
    def pause_timer(self):
        """暫停計時器"""
        if self.running and not self.paused:
            self.paused = True
            self.paused_at = time.time()
    
    def reset_timer(self):
        """重置計時器"""
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        self.paused_at = 0
    
    def set_countdown(self, minutes: int):
        """設置倒數計時器"""
        self.timer_type = "countdown"
        self.target_time = minutes * 60
        self.reset_timer()
    
    def set_pomodoro(self):
        """設置番茄鐘（25分鐘）"""
        self.timer_type = "pomodoro"
        self.target_time = 25 * 60
        self.reset_timer()
    
    def set_stopwatch(self):
        """設置秒錶模式"""
        self.timer_type = "stopwatch"
        self.target_time = None
        self.reset_timer()
    
    def show_mode_selection(self):
        """顯示模式選擇"""
        self.console.clear()
        
        table = Table(title="⏰ 選擇計時器模式", box=box.ROUNDED)
        table.add_column("選項", style="cyan", width=8)
        table.add_column("模式", style="green")
        table.add_column("說明", style="yellow")
        
        table.add_row("1", "⏱️ 秒錶", "正向計時，適合測量時間")
        table.add_row("2", "⏰ 倒數計時", "倒數計時，可設定時間")
        table.add_row("3", "🍅 番茄鐘", "25分鐘工作計時")
        
        self.console.print(table)
        
        try:
            choice = IntPrompt.ask("請選擇模式", choices=["1", "2", "3"], default=1)
            
            if choice == 1:
                self.set_stopwatch()
            elif choice == 2:
                minutes = IntPrompt.ask("請輸入倒數分鐘數", default=5, min=1, max=999)
                self.set_countdown(minutes)
            elif choice == 3:
                self.set_pomodoro()
        except (KeyboardInterrupt, EOFError):
            pass
    
    def run(self):
        """運行計時器"""
        self.console.clear()
        self.show_mode_selection()
        
        layout = self.create_layout()
        
        try:
            with Live(layout, console=self.console, refresh_per_second=10, screen=True) as live:
                while True:
                    # 更新佈局
                    layout["header"].update(self.create_info_panel())
                    layout["main"].update(self.create_timer_display())
                    layout["controls"].update(self.create_controls_panel())
                    
                    # 檢查倒數計時器是否結束
                    if (self.timer_type in ["countdown", "pomodoro"] and 
                        self.running and not self.paused and 
                        self.get_current_time() <= 0):
                        
                        # 時間到，發出提醒
                        self.running = False
                        live.update(layout)
                        
                        # 播放提醒音（如果可能）
                        try:
                            import os
                            os.system("say '時間到了!'")  # macOS
                        except:
                            pass
                        
                        # 等待用戶按鍵繼續
                        self.console.print("\n[red bold]⏰ 時間到了！按任意鍵繼續...[/]", justify="center")
                        input()
                        self.reset_timer()
                    
                    # 檢查按鍵（非阻塞）
                    try:
                        if keyboard.is_pressed('space'):
                            if self.running and not self.paused:
                                self.pause_timer()
                            else:
                                self.start_timer()
                            time.sleep(0.2)  # 防止重複觸發
                            
                        elif keyboard.is_pressed('r'):
                            self.reset_timer()
                            time.sleep(0.2)
                            
                        elif keyboard.is_pressed('m'):
                            live.stop()
                            self.show_mode_selection()
                            live.start()
                            time.sleep(0.2)
                            
                        elif keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
                            break
                            
                    except:
                        # 如果 keyboard 庫不可用，使用替代方案
                        pass
                    
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            pass
        
        self.console.print("\n[green]謝謝使用 Rich 計時器！[/] 👋", justify="center")

def main():
    """主程式"""
    print("🚀 啟動 Rich 計時器...")
    
    try:
        timer = RichTimer()
        timer.run()
    except KeyboardInterrupt:
        print("\n👋 再見！")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    main()
