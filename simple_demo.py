#!/usr/bin/env python3
"""
PyTermGUI 簡單示範 - 展示基本 widgets
"""

import pytermgui as ptg

def main():
    # 基本配色設定
    ptg.tim.define("!title", ptg.tim.parse("[bold 154]"))
    ptg.tim.define("!info", ptg.tim.parse("[dim 245]"))
    
    # 建立視窗
    with ptg.WindowManager() as manager:
        window = ptg.Window(
            "[!title]PyTermGUI 基本功能",
            "",
            "[!info]這是一個簡單的 TUI 應用程式示範",
            "",
            # 各種基本 widgets
            ptg.Label("標籤 (Label)"),
            ptg.InputField("輸入文字...", prompt="輸入: "),
            "",
            ptg.Checkbox("這是一個核取方塊"),
            "",
            ptg.Button("按鈕 1", lambda: print("按鈕 1 被點擊!")),
            ptg.Button("按鈕 2", lambda: print("按鈕 2 被點擊!")),
            "",
            ptg.ProgressBar(30, 100, width=40),  # 30% 進度
            "",
            ptg.Button("離開", lambda *_: manager.stop()),
            width=50
        )
        
        window.center()
        manager.add(window)

if __name__ == "__main__":
    main()
