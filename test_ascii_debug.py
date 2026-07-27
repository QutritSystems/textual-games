#!/usr/bin/env python3
"""
Debug test for ASCII Art Generator
"""

import sys
sys.path.append('/Users/databird/textual-games')

from ascii_art_generator import ASCIIArtGenerator

def test_ascii_generation():
    """Test ASCII art generation independently"""
    
    app = ASCIIArtGenerator()
    
    # Test font data
    print("Testing font data...")
    big_font = app.fonts.get("Big", {})
    print(f"Big font has {len(big_font)} characters")
    
    # Test A character
    if 'A' in big_font:
        print("Letter 'A' in Big font:")
        for line in big_font['A']:
            print(f"'{line}'")
    
    print("\n" + "="*50 + "\n")
    
    # Test art generation directly
    print("Testing art generation for 'HELLO'...")
    
    text = "HELLO"
    text = text.upper()[:20]
    font = app.fonts.get("Big", app.fonts["Big"])
    
    # Get font height
    font_height = len(list(font.values())[0]) if font else 5
    print(f"Font height: {font_height}")
    
    # Generate lines
    art_lines = [""] * font_height
    
    for char in text:
        print(f"Processing character: '{char}'")
        if char in font:
            char_lines = font[char]
            print(f"Character lines: {char_lines}")
            for i in range(font_height):
                art_lines[i] += char_lines[i] + " "
        else:
            print(f"Character '{char}' not found in font!")
    
    print("\nGenerated art lines:")
    for i, line in enumerate(art_lines):
        print(f"Line {i}: '{line}'")
    
    # Apply center alignment
    art_lines = [line.center(60) for line in art_lines]
    
    print("\nAfter centering:")
    for i, line in enumerate(art_lines):
        print(f"Line {i}: '{line}'")
    
    # Join lines
    final_art = "\n".join(art_lines)
    print("\nFinal art:")
    print(final_art)
    
    return final_art

if __name__ == "__main__":
    test_ascii_generation()
