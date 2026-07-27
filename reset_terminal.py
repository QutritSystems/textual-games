#!/usr/bin/env python3
"""
終端重置工具
用於修復虛擬環境中的輸入問題
"""

import sys
import os
import termios
import tty
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def reset_terminal():
    """重置終端設定"""
    console = Console()
    
    console.print("[yellow]正在重置終端設定...[/]")
    
    try:
        # 方法1：使用 stty 命令重置
        subprocess.run(['stty', 'sane'], check=True)
        console.print("✓ [green]stty 重置完成[/]")
    except subprocess.CalledProcessError:
        console.print("❌ [red]stty 重置失敗[/]")
    
    try:
        # 方法2：使用 reset 命令
        subprocess.run(['reset'], check=True)
        console.print("✓ [green]reset 命令執行完成[/]")
    except subprocess.CalledProcessError:
        console.print("❌ [red]reset 命令失敗[/]")
    
    try:
        # 方法3：Python termios 重置
        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            # 設置為正常模式
            new_settings = termios.tcgetattr(fd)
            new_settings[3] = new_settings[3] | termios.ECHO | termios.ICANON
            termios.tcsetattr(fd, termios.TCSANOW, new_settings)
            console.print("✓ [green]termios 重置完成[/]")
        else:
            console.print("⚠️ [yellow]不是 TTY，跳過 termios 重置[/]")
    except Exception as e:
        console.print(f"❌ [red]termios 重置失敗: {e}[/]")
    
    console.print("[green]終端重置完成！[/]")

def diagnose_terminal():
    """診斷終端環境"""
    console = Console()
    
    table = Table(title="🔍 終端環境診斷")
    table.add_column("項目", style="cyan")
    table.add_column("值", style="green")
    table.add_column("狀態", style="yellow")
    
    # 檢查 TERM 變數
    term = os.environ.get('TERM', 'unknown')
    status = "✓ 正常" if term in ['xterm-256color', 'screen-256color', 'tmux-256color'] else "⚠️ 可能有問題"
    table.add_row("TERM", term, status)
    
    # 檢查是否為 TTY
    is_tty = sys.stdin.isatty()
    status = "✓ 是 TTY" if is_tty else "❌ 不是 TTY"
    table.add_row("TTY", str(is_tty), status)
    
    # 檢查虛擬環境
    venv = os.environ.get('VIRTUAL_ENV', '無')
    status = "✓ 在虛擬環境中" if venv != '無' else "⚠️ 不在虛擬環境中"
    table.add_row("虛擬環境", venv, status)
    
    # 檢查 Python 版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    status = "✓ 支援的版本"
    table.add_row("Python版本", python_version, status)
    
    # 檢查終端大小
    try:
        import shutil
        terminal_size = shutil.get_terminal_size()
        size_str = f"{terminal_size.columns}x{terminal_size.lines}"
        status = "✓ 正常" if terminal_size.columns > 80 else "⚠️ 終端較窄"
        table.add_row("終端大小", size_str, status)
    except Exception:
        table.add_row("終端大小", "無法取得", "❌ 錯誤")
    
    # 檢查 locale
    locale_env = os.environ.get('LC_ALL', os.environ.get('LANG', 'unknown'))
    status = "✓ UTF-8" if 'UTF-8' in locale_env.upper() else "⚠️ 可能不支援 UTF-8"
    table.add_row("Locale", locale_env, status)
    
    console.print(table)

def test_input():
    """測試輸入功能"""
    console = Console()
    
    console.print(Panel("🧪 輸入測試", style="blue"))
    console.print("請輸入一些文字來測試輸入是否正常工作：")
    
    try:
        user_input = input("輸入測試 > ")
        console.print(f"✓ [green]成功接收輸入: '{user_input}'[/]")
        
        # 測試特殊字符
        console.print("請輸入一個空格然後按 Enter：")
        space_input = input("空格測試 > ")
        if space_input == " ":
            console.print("✓ [green]空格輸入正常[/]")
        else:
            console.print(f"⚠️ [yellow]空格輸入異常: '{repr(space_input)}'[/]")
            
    except Exception as e:
        console.print(f"❌ [red]輸入測試失敗: {e}[/]")

def main():
    """主程式"""
    console = Console()
    
    console.print(Panel.fit(
        "[bold cyan]終端重置工具[/]\n"
        "用於修復虛擬環境中的輸入問題",
        style="blue"
    ))
    
    while True:
        console.print("\n選擇操作:")
        console.print("1. 📊 診斷終端環境")
        console.print("2. 🔄 重置終端設定")  
        console.print("3. 🧪 測試輸入功能")
        console.print("4. ❌ 退出")
        
        try:
            choice = input("\n請選擇 [1-4]: ").strip()
            
            if choice == '1':
                console.print()
                diagnose_terminal()
            elif choice == '2':
                console.print()
                reset_terminal()
            elif choice == '3':
                console.print()
                test_input()
            elif choice == '4':
                console.print("[green]再見！[/]")
                break
            else:
                console.print("❌ [red]無效選擇，請輸入 1-4[/]")
                
        except KeyboardInterrupt:
            console.print("\n[green]再見！[/]")
            break
        except EOFError:
            console.print("\n[yellow]輸入結束[/]")
            break

if __name__ == "__main__":
    main()
