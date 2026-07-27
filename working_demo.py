#!/usr/bin/env python3
"""
PyTermGUI 實際工作示範 - 一個簡單的計算器 UI
"""

import pytermgui as ptg

def create_calculator():
    """創建一個簡單的計算器界面"""
    
    # 結果顯示
    result_display = ptg.Label("0", width=30)
    current_input = ptg.InputField("", prompt="輸入: ")
    
    def calculate():
        try:
            expr = current_input.value
            if expr.strip():
                result = eval(expr)  # 注意：實際應用中不應使用 eval
                result_display.value = f"結果: {result}"
                current_input.value = ""
            else:
                result_display.value = "請輸入計算式"
        except Exception as e:
            result_display.value = f"錯誤: {str(e)}"
    
    def clear():
        current_input.value = ""
        result_display.value = "0"
    
    # 創建主窗口
    with ptg.WindowManager() as manager:
        window = ptg.Window(
            "[bold]簡單計算器",
            "",
            result_display,
            "",
            current_input,
            "",
            ptg.Container(
                ptg.Button("計算", lambda *_: calculate()),
                ptg.Button("清除", lambda *_: clear()),
                ptg.Button("離開", lambda *_: manager.stop())
            ),
            width=40
        )
        
        window.center()
        manager.add(window)

def create_todo_app():
    """創建一個簡單的 Todo 應用"""
    
    todos = []
    todo_container = ptg.Container()
    input_field = ptg.InputField("", prompt="新任務: ")
    
    def add_todo():
        task = input_field.value.strip()
        if task:
            todos.append({"task": task, "done": False})
            input_field.value = ""
            update_todo_display()
    
    def update_todo_display():
        # 清空容器
        todo_container.clear()
        
        # 添加所有 todos
        for i, todo in enumerate(todos):
            status = "✓" if todo["done"] else "○"
            label = f"{status} {todo['task']}"
            
            # 創建一個包含任務和刪除按鈕的容器
            task_container = ptg.Container(
                ptg.Label(label),
                ptg.Button("刪除", lambda idx=i: remove_todo(idx))
            )
            todo_container += task_container
    
    def remove_todo(index):
        if 0 <= index < len(todos):
            todos.pop(index)
            update_todo_display()
    
    # 創建主窗口
    with ptg.WindowManager() as manager:
        window = ptg.Window(
            "[bold]Todo 應用程式",
            "",
            input_field,
            "",
            ptg.Button("新增任務", lambda *_: add_todo()),
            "",
            "[dim]--- 任務列表 ---",
            todo_container,
            "",
            ptg.Button("離開", lambda *_: manager.stop()),
            width=50
        )
        
        window.center()
        manager.add(window)

def main_menu():
    """主選單"""
    
    with ptg.WindowManager() as manager:
        window = ptg.Window(
            "[bold]PyTermGUI 示範選單",
            "",
            "[dim]選擇一個示範應用:",
            "",
            ptg.Button("計算器", lambda *_: run_calculator(manager)),
            ptg.Button("Todo 應用", lambda *_: run_todo_app(manager)),
            "",
            ptg.Button("離開", lambda *_: manager.stop()),
            width=30
        )
        
        window.center()
        manager.add(window)

def run_calculator(manager):
    """運行計算器"""
    manager.stop()  # 停止當前管理器
    create_calculator()  # 啟動計算器

def run_todo_app(manager):
    """運行 Todo 應用"""
    manager.stop()  # 停止當前管理器
    create_todo_app()  # 啟動 Todo 應用

if __name__ == "__main__":
    print("PyTermGUI 基本功能示範")
    print("=" * 30)
    print("\n這個示範包含:")
    print("1. 簡單計算器 - 展示輸入、按鈕、結果顯示")
    print("2. Todo 應用 - 展示動態列表、增刪功能")
    print("\n按 Ctrl+C 可隨時退出應用\n")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n程式已退出，感謝使用！")
