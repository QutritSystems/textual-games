#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ASCII Art Generator
"""

import sys
sys.path.append('.')

from ascii_generator import ASCIIArtGenerator

def test_ascii_generation():
    """Test the ASCII art generation without the TUI."""
    
    print("🎨 Testing ASCII Art Generator...")
    print("=" * 50)
    
    # Create instance
    app = ASCIIArtGenerator()
    
    # Test different styles
    test_words = ["HELLO", "TEST", "ASCII"]
    styles = ["Big", "Block", "Small"]
    
    for word in test_words:
        print(f"\n📝 Testing word: {word}")
        print("-" * 30)
        
        for style in styles:
            print(f"\n🎯 Style: {style}")
            app.selected_style = style
            app.input_text = word
            app.border_enabled = False
            app.alignment = "left"
            
            # Generate ASCII art
            app.generate_ascii_art(word)
            
            # Print the result
            if app.current_art:
                print(app.current_art)
            else:
                print("No art generated!")
    
    # Test with border
    print("\n" + "=" * 50)
    print("🎨 Testing with Border:")
    print("=" * 50)
    
    app.selected_style = "Big"
    app.input_text = "BORDER"
    app.border_enabled = True
    app.alignment = "center"
    app.generate_ascii_art("BORDER")
    
    if app.current_art:
        print(app.current_art)
    else:
        print("No border art generated!")
    
    print("\n✅ ASCII Art Generator test completed!")

if __name__ == "__main__":
    test_ascii_generation()
