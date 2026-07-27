#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone ASCII Art Generator Test
"""

class SimpleASCIIGenerator:
    """Simple ASCII Art Generator for testing."""
    
    def __init__(self):
        # ASCII font patterns using only basic ASCII characters
        self.fonts = {
            "Big": {
                'A': [" ##### ", "##   ##", "#######", "##   ##", "##   ##"],
                'B': ["###### ", "##   ##", "###### ", "##   ##", "###### "],
                'C': [" ######", "##     ", "##     ", "##     ", " ######"],
                'D': ["###### ", "##   ##", "##   ##", "##   ##", "###### "],
                'E': ["#######", "##     ", "#####  ", "##     ", "#######"],
                'F': ["#######", "##     ", "#####  ", "##     ", "##     "],
                'G': [" ###### ", "##      ", "##   ###", "##    ##", " ###### "],
                'H': ["##   ##", "##   ##", "#######", "##   ##", "##   ##"],
                'I': ["#######", "   ##  ", "   ##  ", "   ##  ", "#######"],
                'J': ["#######", "     ##", "     ##", "##   ##", " ######"],
                'K': ["##   ##", "##  ## ", "#####  ", "##  ## ", "##   ##"],
                'L': ["##     ", "##     ", "##     ", "##     ", "#######"],
                'M': ["#######", "#######", "## # ##", "##   ##", "##   ##"],
                'N': ["#######", "##   ##", "##   ##", "##   ##", "##   ##"],
                'O': [" ###### ", "##    ##", "##    ##", "##    ##", " ###### "],
                'P': ["###### ", "##   ##", "###### ", "##     ", "##     "],
                'Q': [" ###### ", "##    ##", "## #  ##", "##  # ##", " ###### "],
                'R': ["###### ", "##   ##", "###### ", "##   ##", "##   ##"],
                'S': [" ######", "##     ", " ##### ", "     ##", "###### "],
                'T': ["#######", "   ##  ", "   ##  ", "   ##  ", "   ##  "],
                'U': ["##   ##", "##   ##", "##   ##", "##   ##", " ######"],
                'V': ["##   ##", "##   ##", "##   ##", " ## ## ", "  ###  "],
                'W': ["##   ##", "##   ##", "## # ##", "#######", "#######"],
                'X': ["##   ##", " ## ## ", "  ###  ", " ## ## ", "##   ##"],
                'Y': ["##   ##", " ## ## ", "  ###  ", "   ##  ", "   ##  "],
                'Z': ["#######", "    ## ", "   ##  ", "  ##   ", "#######"],
                ' ': ["       ", "       ", "       ", "       ", "       "],
                '!': ["  ##   ", "  ##   ", "  ##   ", "       ", "  ##   "],
                '?': [" ######", "     ##", "  #####", "       ", "   ##  "],
            },
            
            "Block": {
                'A': ["###", "#*#", "###", "# #", "# #"],
                'B': ["## ", "#*#", "## ", "#*#", "## "],
                'C': ["###", "#  ", "#  ", "#  ", "###"],
                'D': ["## ", "# #", "# #", "# #", "## "],
                'E': ["###", "#  ", "## ", "#  ", "###"],
                'F': ["###", "#  ", "## ", "#  ", "#  "],
                'G': ["###", "#  ", "#*#", "# #", "###"],
                'H': ["# #", "# #", "###", "# #", "# #"],
                'I': ["###", " # ", " # ", " # ", "###"],
                'J': ["###", "  #", "  #", "# #", "###"],
                'K': ["# #", "## ", "#* ", "# #", "# #"],
                'L': ["#  ", "#  ", "#  ", "#  ", "###"],
                'M': ["###", "###", "#*#", "# #", "# #"],
                'N': ["###", "# #", "# #", "# #", "# #"],
                'O': ["###", "# #", "# #", "# #", "###"],
                'P': ["## ", "# #", "## ", "#  ", "#  "],
                'Q': ["###", "# #", "#*#", "#*#", "###"],
                'R': ["## ", "# #", "## ", "# #", "# #"],
                'S': ["###", "#  ", "###", "  #", "###"],
                'T': ["###", " # ", " # ", " # ", " # "],
                'U': ["# #", "# #", "# #", "# #", "###"],
                'V': ["# #", "# #", "# #", "*#*", " # "],
                'W': ["# #", "# #", "#*#", "###", "###"],
                'X': ["# #", "*#*", " # ", "*#*", "# #"],
                'Y': ["# #", "*#*", " # ", " # ", " # "],
                'Z': ["###", " # ", " # ", " # ", "###"],
                ' ': ["   ", "   ", "   ", "   ", "   "],
                '!': [" # ", " # ", " # ", "   ", " # "],
                '?': ["## ", " # ", " # ", "   ", " # "],
            },
            
            "Small": {
                'A': ["#*#", "#*#", "# #"],
                'B': ["#*|", "#*|", "#*/"],
                'C': ["/*#", "#--", "---"],
                'D': ["#*|", "# #", "#*/"],
                'E': ["#--", "#--", "#--"],
                'F': ["#--", "#--", "#  "],
                'G': ["/*#", "#*#", "--#"],
                'H': ["# #", "###", "# #"],
                'I': ["###", " # ", "###"],
                'J': ["###", "  #", "## "],
                'K': ["# #", "## ", "# #"],
                'L': ["#  ", "#  ", "###"],
                'M': ["###", "#*#", "# #"],
                'N': ["##*", "#*#", "# #"],
                'O': ["/*#", "# #", "---"],
                'P': ["#*|", "#* ", "#  "],
                'Q': ["/*#", "#*#", "---"],
                'R': ["#*|", "#*|", "# #"],
                'S': ["/--", "--/", "--/"],
                'T': ["###", " # ", " # "],
                'U': ["# #", "# #", "---"],
                'V': ["# #", "# #", " * "],
                'W': ["# #", "#*#", "###"],
                'X': ["# #", " * ", "# #"],
                'Y': ["# #", " * ", " # "],
                'Z': ["###", " * ", "###"],
                ' ': ["   ", "   ", "   "],
                '!': [" # ", " # ", " # "],
                '?': ["--/", " /*", " # "],
            }
        }
        
    def generate_ascii_art(self, text: str, style: str = "Big", alignment: str = "left", border: bool = False) -> str:
        """Generate ASCII art from text."""
        if not text:
            return ""
        
        text = text.upper()[:12]  # Limit to 12 characters
        font = self.fonts.get(style, self.fonts["Big"])
        
        # Get font height
        font_height = len(list(font.values())[0]) if font else 5
        
        # Generate lines
        art_lines = [""] * font_height
        
        for char in text:
            if char in font:
                char_lines = font[char]
                for i in range(font_height):
                    art_lines[i] += char_lines[i] + " "
        
        # Apply alignment
        if alignment == "center":
            art_lines = [line.center(60) for line in art_lines]
        elif alignment == "right":
            art_lines = [line.rjust(60) for line in art_lines]
        
        # Add border if enabled
        if border:
            max_width = max(len(line.rstrip()) for line in art_lines) + 4
            
            # Top border
            bordered_lines = ["+" + "-" * (max_width - 2) + "+"]
            
            # Content with side borders
            for line in art_lines:
                padded_line = line.ljust(max_width - 4)
                bordered_lines.append(f"| {padded_line} |")
            
            # Bottom border
            bordered_lines.append("+" + "-" * (max_width - 2) + "+")
            
            art_lines = bordered_lines
        
        return "\n".join(art_lines)


def test_ascii_generation():
    """Test the ASCII art generation."""
    
    print("🎨 Testing ASCII Art Generator...")
    print("=" * 50)
    
    # Create instance
    generator = SimpleASCIIGenerator()
    
    # Test different styles
    test_words = ["HELLO", "TEST", "ASCII"]
    styles = ["Big", "Block", "Small"]
    
    for word in test_words:
        print(f"\n📝 Testing word: {word}")
        print("-" * 30)
        
        for style in styles:
            print(f"\n🎯 Style: {style}")
            art = generator.generate_ascii_art(word, style, "left", False)
            if art:
                print(art)
            else:
                print("No art generated!")
    
    # Test with border
    print("\n" + "=" * 50)
    print("🎨 Testing with Border:")
    print("=" * 50)
    
    art = generator.generate_ascii_art("BORDER", "Big", "center", True)
    if art:
        print(art)
    else:
        print("No border art generated!")
    
    # Save test art to file
    print("\n" + "=" * 50)
    print("💾 Saving Test Art to File:")
    print("=" * 50)
    
    test_art = generator.generate_ascii_art("TEXTUAL", "Big", "center", True)
    
    try:
        filename = "test_ascii_output.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("ASCII Art Generator Test Output\n")
            f.write("Text: 'TEXTUAL', Style: Big, Border: True\n")
            f.write("=" * 50 + "\n\n")
            f.write(test_art)
            f.write("\n\n" + "=" * 50 + "\n")
            f.write("Generated with Standalone ASCII Art Generator\n")
        
        print(f"✅ Test art saved as {filename}")
        print(f"📄 Preview:\n{test_art}")
    except Exception as e:
        print(f"❌ Save failed: {str(e)}")
    
    print("\n✅ ASCII Art Generator test completed!")


if __name__ == "__main__":
    test_ascii_generation()
