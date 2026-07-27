#!/usr/bin/env python3
"""
PyTermGUI 命令行示範 - 展示各種 widgets 的創建和基本用法
"""

import pytermgui as ptg

def demonstrate_widgets():
    """示範各種 PyTermGUI widgets"""
    
    print("=== PyTermGUI 基本功能示範 ===\n")
    
    # 1. Label (標籤)
    print("1. Label (標籤):")
    label = ptg.Label("這是一個標籤")
    print(f"   建立的標籤: {label}")
    print(f"   標籤內容: {label.value}\n")
    
    # 2. Button (按鈕)  
    print("2. Button (按鈕):")
    button = ptg.Button("點擊我", lambda: print("按鈕被點擊了!"))
    print(f"   建立的按鈕: {button}")
    print(f"   按鈕標籤: {button.label}\n")
    
    # 3. InputField (輸入框)
    print("3. InputField (輸入框):")
    input_field = ptg.InputField("Default text", prompt="Input: ")
    print(f"   建立的輸入框: {input_field}")
    print(f"   輸入框提示: {input_field.prompt}")
    print(f"   預設值: {input_field.value}\n")
    
    # 4. Checkbox (核取方塊)
    print("4. Checkbox (核取方塊):")
    checkbox = ptg.Checkbox("選項 1", checked=True)
    print(f"   建立的核取方塊: {checkbox}")
    print(f"   是否被勾選: {checkbox.checked}\n")
    
    # 5. Splitter (分割器)
    print("5. Splitter (分割器):")
    splitter = ptg.Splitter(
        ptg.Label("左側區域"),
        ptg.Label("右側區域")
    )
    print(f"   建立的分割器: {splitter}")
    print(f"   分割器子組件數量: {len(list(splitter))}\n")
    
    # 6. Container (容器)
    print("6. Container (容器):")
    container = ptg.Container(
        ptg.Label("容器內的標籤 1"),
        ptg.Label("容器內的標籤 2"),
        ptg.Button("容器內的按鈕", lambda: None)
    )
    print(f"   建立的容器: {container}")
    print(f"   容器內 widget 數量: {len(container)}\n")
    
    # 7. 顏色和樣式
    print("7. 顏色和樣式 (TIM - Terminal Interface Markup):")
    
    # 定義樣式
    ptg.tim.define("!success", ptg.tim.parse("[green bold]"))
    ptg.tim.define("!warning", ptg.tim.parse("[yellow]"))
    ptg.tim.define("!error", ptg.tim.parse("[red bold]"))
    
    styled_labels = [
        ptg.Label("[!success]成功訊息"),
        ptg.Label("[!warning]警告訊息"), 
        ptg.Label("[!error]錯誤訊息")
    ]
    
    for label in styled_labels:
        print(f"   {label}\n")
    
    print("=== PyTermGUI 主要特點 ===")
    print("• 豐富的 widgets: Button, Label, InputField, Checkbox, ProgressBar...")
    print("• 靈活的佈局系統: Container, Window...")
    print("• 內建樣式系統: TIM (Terminal Interface Markup)")
    print("• 響應式設計: 支援終端大小調整")
    print("• 事件處理: 鍵盤和滑鼠事件")
    print("• 主題支援: 可自訂顏色和樣式")

def demonstrate_window_manager():
    """示範視窗管理器的基本概念"""
    print("\n=== 視窗管理概念 ===")
    print("PyTermGUI 使用 WindowManager 來管理多個視窗:")
    print("• WindowManager: 管理所有視窗的主控制器")
    print("• Window: 包含 widgets 的容器") 
    print("• 支援多視窗、對話框、彈出視窗")
    print("• 自動處理焦點、鍵盤導航等")
    
def main():
    """主函數"""
    demonstrate_widgets()
    demonstrate_window_manager()
    
    print("\n=== 如何運行互動式示範 ===")
    print("運行以下命令來體驗完整的互動式界面:")
    print("source pytermgui_env/bin/activate && python3 simple_demo.py")

if __name__ == "__main__":
    main()
