#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to check ASCII Art display functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ascii_test_standalone import SimpleASCIIGenerator

def test_display():
    """Test ASCII art display functionality."""
    
    print("🔍 Debug: Testing ASCII Art Display Functionality")
    print("=" * 60)
    
    # Test 1: Basic generation
    print("\n📋 Test 1: Basic ASCII generation")
    generator = SimpleASCIIGenerator()
    
    test_word = "TEST"
    art = generator.generate_ascii_art(test_word, "Big", "left", False)
    
    print(f"Input: {test_word}")
    print(f"Output length: {len(art)} chars")
    print(f"Output lines: {art.count(chr(10)) + 1 if art else 0}")
    print("Generated Art:")
    print("-" * 40)
    print(art)
    print("-" * 40)
    
    # Test 2: Different styles
    print("\n📋 Test 2: Different font styles")
    styles = ["Big", "Block", "Small"]
    for style in styles:
        art = generator.generate_ascii_art("HI", style, "left", False)
        print(f"\nStyle: {style}")
        print(f"Lines: {art.count(chr(10)) + 1 if art else 0}")
        print(art)
    
    # Test 3: Alignment
    print("\n📋 Test 3: Alignment test")
    alignments = ["left", "center", "right"]
    for align in alignments:
        art = generator.generate_ascii_art("OK", "Block", align, False)
        print(f"\nAlignment: {align}")
        print(art)
        
    # Test 4: Border
    print("\n📋 Test 4: Border test")
    art = generator.generate_ascii_art("BOX", "Block", "center", True)
    print("With Border:")
    print(art)
    
    print("\n✅ Display functionality tests completed!")
    print(f"🎯 All tests show ASCII art should be visible in the Textual interface.")
    print(f"🖥️  If you don't see ASCII art in the app, it might be a height/scrolling issue.")

if __name__ == "__main__":
    test_display()
