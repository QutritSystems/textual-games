#!/usr/bin/env python3
"""
Comprehensive test script for all Textual games
Tests imports, creation, CSS parsing, and basic functionality
"""

import sys
import traceback

def test_game_launcher():
    """Test Game Launcher"""
    print("🚀 Testing Game Launcher...")
    try:
        from game_launcher import GameLauncher
        app = GameLauncher()
        print("✅ GameLauncher created successfully")
        print(f"   - Title: {app.title}")
        print(f"   - CSS length: {len(app.CSS)} characters")
        return True
    except Exception as e:
        print(f"❌ GameLauncher error: {e}")
        traceback.print_exc()
        return False

def test_snake_game():
    """Test Snake Game"""
    print("\n🐍 Testing Snake Game...")
    try:
        from snake_game import SnakeGame, Direction
        app = SnakeGame()
        print("✅ SnakeGame created successfully")
        print(f"   - Title: {app.title}")
        print(f"   - Grid size: {app.grid_width}x{app.grid_height}")
        print(f"   - Initial snake length: {len(app.snake)}")
        print(f"   - Direction enum: {Direction.UP.value}")
        print(f"   - CSS length: {len(app.CSS)} characters")
        
        # Test game state
        app.spawn_food()
        print(f"   - Food spawned at: {app.food}")
        
        return True
    except Exception as e:
        print(f"❌ SnakeGame error: {e}")
        traceback.print_exc()
        return False

def test_number_guessing():
    """Test Number Guessing Game"""
    print("\n🎯 Testing Number Guessing Game...")
    try:
        from number_guessing_game import NumberGuessingGame
        app = NumberGuessingGame()
        print("✅ NumberGuessingGame created successfully")
        print(f"   - Title: {app.title}")
        print(f"   - Difficulty: {app.difficulty}")
        print(f"   - Range: {app.min_number}-{app.max_number}")
        print(f"   - Max attempts: {app.max_attempts}")
        print(f"   - Difficulty levels: {list(app.difficulty_settings.keys())}")
        print(f"   - CSS length: {len(app.CSS)} characters")
        
        # Test difficulty settings
        for diff, (min_n, max_n, attempts) in app.difficulty_settings.items():
            print(f"   - {diff}: {min_n}-{max_n}, {attempts} attempts")
            
        return True
    except Exception as e:
        print(f"❌ NumberGuessingGame error: {e}")
        traceback.print_exc()
        return False

def test_ascii_art_generator():
    """Test ASCII Art Generator"""
    print("\n🎨 Testing ASCII Art Generator...")
    try:
        from ascii_art_generator import ASCIIArtGenerator
        app = ASCIIArtGenerator()
        print("✅ ASCIIArtGenerator created successfully")
        print(f"   - Title: {app.title}")
        print(f"   - Font styles: {list(app.fonts.keys())}")
        print(f"   - Border styles: {list(app.borders.keys())}")
        print(f"   - CSS length: {len(app.CSS)} characters")
        
        # Test font data
        for style, font_data in app.fonts.items():
            char_count = len(font_data)
            height = len(list(font_data.values())[0]) if font_data else 0
            print(f"   - {style} font: {char_count} chars, {height} rows")
        
        return True
    except Exception as e:
        print(f"❌ ASCIIArtGenerator error: {e}")
        traceback.print_exc()
        return False

def test_widgets():
    """Test widget imports and creation"""
    print("\n🧪 Testing Textual widgets...")
    try:
        from textual.widgets import (
            Button, Label, Static, Input, Header, Footer,
            ProgressBar, Select
        )
        from textual.containers import Container, Horizontal, Vertical
        from textual.reactive import reactive
        
        # Test widget creation
        widgets = [
            Button("Test"),
            Label("Test"),
            Static("Test"),
            Input(placeholder="Test"),
            ProgressBar(total=100),
            Select([("Option 1", "1")]),
            Container(),
            Horizontal(),
            Vertical()
        ]
        
        print(f"✅ All {len(widgets)} widget types created successfully")
        
        # Test reactive
        class TestReactive:
            counter = reactive(0)
        
        # Note: Can't actually set reactive value without proper initialization
        print("✅ Reactive import successful")
        
        return True
    except Exception as e:
        print(f"❌ Widget test error: {e}")
        traceback.print_exc()
        return False

def test_css_parsing():
    """Test CSS parsing in all games"""
    print("\n🎨 Testing CSS parsing...")
    
    css_tests = [
        ("GameLauncher", "game_launcher", "GameLauncher"),
        ("SnakeGame", "snake_game", "SnakeGame"),
        ("NumberGuessingGame", "number_guessing_game", "NumberGuessingGame")
    ]
    
    all_passed = True
    
    for display_name, module_name, class_name in css_tests:
        try:
            module = __import__(module_name)
            game_class = getattr(module, class_name)
            
            # Create instance to trigger CSS parsing
            app = game_class()
            
            print(f"✅ {display_name} CSS parsed successfully")
            
            # Check for common CSS issues
            css = app.CSS
            if "font-weight" in css:
                print(f"⚠️  {display_name} contains font-weight (not supported)")
            if "font-style" in css:
                print(f"⚠️  {display_name} contains font-style (not supported)")
            if "font-family" in css:
                print(f"⚠️  {display_name} contains font-family (not supported)")
                
        except Exception as e:
            print(f"❌ {display_name} CSS error: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("🧪 Textual Games - Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Widget Tests", test_widgets),
        ("CSS Parsing", test_css_parsing),
        ("Game Launcher", test_game_launcher),
        ("Snake Game", test_snake_game),
        ("Number Guessing", test_number_guessing),
        ("ASCII Art Generator", test_ascii_art_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Games are ready to play!")
        print("\n🎮 Quick Start:")
        print("   ./play.sh launcher    # Start game launcher")
        print("   ./play.sh snake      # Play Snake Game")
        print("   ./play.sh guess      # Play Number Guessing")
        print("   ./play.sh ascii      # Create ASCII Art")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
