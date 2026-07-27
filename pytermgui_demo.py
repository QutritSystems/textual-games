#!/usr/bin/env python3
"""
PyTermGUI 基本功能示範
包含各種 widgets 和佈局功能
"""

import pytermgui as ptg

def main():
    # 設置配色主題
    ptg.tim.define("!title", ptg.tim.parse("[210 bold]"))
    ptg.tim.define("!button", ptg.tim.parse("[157 bold]"))
    
    # 創建主窗口
    with ptg.WindowManager() as manager:
        # 創建一個窗口
        window = ptg.Window(
            # 標題
            "[!title]PyTermGUI 基本功能示範",
            "",
            # 按鈕容器
            ptg.Container(
                "[!button]歡迎使用 PyTermGUI!",
                "",
                # 輸入框
                ptg.InputField("請輸入您的名字...", prompt="姓名: "),
                "",
                # 按鈕
                ptg.Button("按我問候", lambda *_: show_greeting(window)),
                ptg.Button("顯示進度條", lambda *_: show_progressbar(window)),
                ptg.Button("顯示選單", lambda *_: show_menu(window)),
                "",
                ptg.Button("離開", lambda *_: manager.stop()),
            ),
            width=60,
        )
        
        # 設置窗口位置
        window.center()
        manager.add(window)

def show_greeting(window):
    """顯示問候訊息"""
    input_field = None
    for widget in window:
        if isinstance(widget, ptg.Container):
            for child in widget:
                if isinstance(child, ptg.InputField):
                    input_field = child
                    break
    
    if input_field and input_field.value:
        name = input_field.value
        # 創建對話框
        modal = ptg.Window(
            f"你好，{name}！",
            "",
            "歡迎來到 PyTermGUI 的世界！",
            "",
            ptg.Button("確定", lambda *_: modal.close()),
            width=40,
        )
        modal.center()
        ptg.WindowManager.get_manager().add(modal)

def show_progressbar(window):
    """顯示進度條示範"""
    import time
    import threading
    
    progress_window = ptg.Window(
        "進度條示範",
        "",
        ptg.ProgressBar(0, 100, width=40),
        "",
        ptg.Button("關閉", lambda *_: progress_window.close()),
        width=50,
    )
    
    progress_window.center()
    ptg.WindowManager.get_manager().add(progress_window)
    
    # 在背景執行進度更新
    def update_progress():
        progress_bar = None
        for widget in progress_window:
            if isinstance(widget, ptg.ProgressBar):
                progress_bar = widget
                break
        
        if progress_bar:
            for i in range(101):
                progress_bar.value = i
                time.sleep(0.05)
    
    thread = threading.Thread(target=update_progress)
    thread.daemon = True
    thread.start()

def show_menu(window):
    """顯示選擇選單"""
    options = ["選項 1", "選項 2", "選項 3", "返回"]
    
    def handle_selection(_, index):
        if index == len(options) - 1:  # 返回選項
            menu_window.close()
        else:
            result_window = ptg.Window(
                "您的選擇",
                "",
                f"您選擇了: {options[index]}",
                "",
                ptg.Button("確定", lambda *_: result_window.close()),
                width=30,
            )
            result_window.center()
            ptg.WindowManager.get_manager().add(result_window)
    
    menu_window = ptg.Window(
        "選擇選單",
        "",
        ptg.Selector(options, onselect=handle_selection),
        width=25,
    )
    
    menu_window.center()
    ptg.WindowManager.get_manager().add(menu_window)

if __name__ == "__main__":
    main()
