import xml.etree.ElementTree as ET
from util import Rectangle, compare_strings_ignore_trailing_numbers, custom_round, rectangles_are_equal

class XmlParser:
    def __init__(self, scale : float):
        self.scale : float = scale
        self.sprites_coordinates : list[Rectangle] = []

    def load(self, file_path : str):
        """Loads the XML file and returns the parsed XML."""
        self.xml_root = ET.parse(file_path).getroot()
        print(f"Loading {file_path}...")
        print("Loaded!")

    def get_sprite_attributes(self, attribute_names : list[str]) -> list[str]:
        """Returns a list of values of the specified attributes."""
        sprite_attributes = []

        for element in self.xml_root.findall("SubTexture"):
            sprite_attributes.append([element.get(attr) for attr in attribute_names])

        return sprite_attributes

    def parse_sprites_coordinates(self, animation_names: list[str]) -> None:
        """Parses the coordinates of the sprites and adds them to self.sprites_coordinates if they meet the criteria."""
        attributes = self.get_sprite_attributes(["name", "x", "y", "width", "height"])

        for animation_name in animation_names:
            for name, x, y, width, height in attributes:
                if not compare_strings_ignore_trailing_numbers(animation_name, name):
                    continue

                sprite_rect = self._create_scaled_sprite_rectangle(int(x), int(y), int(width), int(height))
                
                if not self.sprite_exists(sprite_rect):
                    self.add_sprite_to_list(sprite_rect)

    def _create_scaled_sprite_rectangle(self, x: int, y: int, width: int, height: int) -> Rectangle:
        """Creates a scaled sprite rectangle based on the provided values."""
        scaled_x = custom_round(x * self.scale)
        scaled_y = custom_round(y * self.scale)
        scaled_width = custom_round(width * self.scale)
        scaled_height = custom_round(height * self.scale)

        return Rectangle(x=scaled_x, y=scaled_y, width=scaled_width, height=scaled_height)

    def sprite_exists(self, sprite_rect: Rectangle) -> bool:
        """Checks if the same sprite frame already exists in the sprite list. """
        return any(rectangles_are_equal(sprite_rect, existing_rect) for existing_rect in self.sprites_coordinates)

    def add_sprite_to_list(self, sprite_rect: Rectangle) -> None:
        """ Adds the sprite rectangle to the list of sprite coordinates. """
        self.sprites_coordinates.append(sprite_rect)

