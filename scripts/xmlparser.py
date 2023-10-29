import xml.etree.ElementTree as ET
from util import Rectangle, rectangles_are_equal
import re

def compare_strings_ignore_trailing_numbers(str1: str, str2: str):
    """Check if both strings are the same, ignoring trailing numbers."""
    str1_stripped = re.sub(r"\d+$", "", str1)
    str2_stripped = re.sub(r"\d+$", "", str2)
    return str1_stripped == str2_stripped

def custom_round(value: float):
    """Custom rounding function to round 0.5 up and -0.5 or less down."""
    if value >= 0:
        return int(value + 0.5)
    else:
        return int(value - 0.5)

class XmlParser:
    def __init__(self, scale : float):
        self.scale : float = scale
        self.sprites_coordinates : list[Rectangle] = []

    def load(self, file_path : str):
        """Loads the XML file and returns the parsed XML."""
        self.xml_root = ET.parse(file_path).getroot()
        print(f"Loading {file_path}...")
        print("Loaded!")

    def parse_sprites_coordinates(self, animation_names: list[str], animation_offsets: list[tuple]) -> None:
        """Parses the coordinates of the sprites and adds them to self.sprites_coordinates if they meet the criteria."""
        attributes_names = ["name", "x", "y", "width", "height", "frameX", "frameY"]

        attributes = [[element.get(attr, 0) for attr in attributes_names] for element in self.xml_root.findall("SubTexture")]

        for animation_name, animation_offset in zip(animation_names, animation_offsets):
            for name, x, y, width, height, pos_x, pos_y in attributes:
                if not compare_strings_ignore_trailing_numbers(animation_name, name):
                    continue

                sprite_rect = Rectangle()

                # Convert to float first to avoid trying to convert a string that is a floating-point number to an integer which results in a error
                sprite_rect.x = custom_round(float(x) * self.scale)
                sprite_rect.y = custom_round(float(y) * self.scale)
                sprite_rect.width = custom_round(float(width) * self.scale)
                sprite_rect.height = custom_round(float(height) * self.scale)

                sprite_rect.pos_x = custom_round(float(pos_x) * self.scale)
                sprite_rect.pos_y = custom_round(float(pos_y) * self.scale)

                sprite_rect.pos_x += int(animation_offset[0] * self.scale)
                sprite_rect.pos_y += int(animation_offset[1] * self.scale)
                
                # Check if the same sprite already exists in the sprite list.
                if not any(rectangles_are_equal(sprite_rect, existing_rect) for existing_rect in self.sprites_coordinates):
                    self.sprites_coordinates.append(sprite_rect)