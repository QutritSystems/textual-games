#!/usr/bin/env python3
"""
檢查 PyTermGUI 可用的組件
"""

import pytermgui as ptg

def check_available_components():
    """檢查 PyTermGUI 中可用的組件"""
    print("=== PyTermGUI 可用組件 ===")
    
    # 檢查主要組件
    components = [
        'Label', 'Button', 'InputField', 'Container', 'Window', 'WindowManager',
        'Checkbox', 'ProgressBar', 'Splitter', 'Collapsible', 'Selector'
    ]
    
    available = []
    not_available = []
    
    for component in components:
        if hasattr(ptg, component):
            available.append(component)
        else:
            not_available.append(component)
    
    print("✅ 可用組件:")
    for comp in available:
        print(f"   - {comp}")
    
    if not_available:
        print("\n❌ 不可用組件:")
        for comp in not_available:
            print(f"   - {comp}")
    
    # 檢查子模組
    print("\n=== PyTermGUI 子模組 ===")
    
    # 檢查 widgets 子模組
    try:
        from pytermgui import widgets
        print("✅ widgets 子模組可用")
        
        widget_attrs = [attr for attr in dir(widgets) if not attr.startswith('_')]
        print("   widgets 子模組內容:")
        for attr in widget_attrs[:10]:  # 只顯示前10個
            print(f"     - {attr}")
        if len(widget_attrs) > 10:
            print(f"     ... 還有 {len(widget_attrs) - 10} 個組件")
            
    except ImportError:
        print("❌ widgets 子模組不可用")
    
    # 檢查是否有 ProgressBar
    try:
        from pytermgui.widgets import ProgressBar
        print("\n✅ ProgressBar 在 widgets 子模組中找到")
    except ImportError:
        print("\n❌ ProgressBar 未找到")

if __name__ == "__main__":
    check_available_components()
