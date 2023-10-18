import xml.etree.ElementTree as ET
from PIL import Image
from util import Rectangle, rectangles_collided
from xmlparser import FNFXmlParser

# Path to the spritesheet file
SPRITESHEET_FILE_PATH = "example/BOYFRIEND"
# Base name for sprite image files
BASE_IMAGE_NAME = "bf"
# Scaling factor to resize the sprites
SCALE_FACTOR = 0.25

# Max image size
MAX_WIDTH = 256
MAX_HEIGHT = 256

# Names of animations to be extracted from the XML file
ANIMATION_NAMES = ["BF idle dance", "BF NOTE LEFT", "BF NOTE DOWN", "BF NOTE UP", "BF NOTE RIGHT"]

def load_image(file_path):
    """Loads the PNG file and return it."""
    png_file = Image.open(file_path)
    print(f"Loading {file_path}...")
    print("Loaded!")

    return png_file

def get_sprites_coordinates(xml_attributes: list[Rectangle], spritesheet: Image) -> list[Rectangle]:
    """
        Returns a sprite coordinate list. The main difference from the XML list is that this function 
        will remove any empty space that the sprite could have, ensuring efficient packing.
    """
    sprites_rect: list[Rectangle] = []

    for attribute in xml_attributes:
        # Crop the sprite using the XML list provided
        sprite = spritesheet.crop((attribute.x, attribute.y, attribute.width + attribute.x, attribute.height + attribute.y))

        # Check if the sprite has valid content
        if sprite.getbbox() is None:
            raise TypeError("Failed to pack sprites; check if your spritesheet has empty sprite spaces or if the XML scale is correct")

        bbox = sprite.getbbox()

        # Create a sprite rectangle without having empty space
        sprite_rect = Rectangle(
            x=attribute.x + bbox[0],
            y=attribute.y + bbox[1],
            width=bbox[2] - bbox[0],
            height=bbox[3] - bbox[1]
        )

        sprites_rect.append(sprite_rect)

    return sprites_rect

def organize_sprite_positions(sprites_rect: list[Rectangle]) -> list[Rectangle]:
    """Returns an organized sprite list that will be used for packing the images."""
    organized_sprites: list[Rectangle] = []
    current_pos_x = 0
    current_pos_y = 0
    current_counter = 0

    for i in sprites_rect:
        sprite_rect = Rectangle(
            x=i.x,
            y=i.y,
            width=i.width,
            height=i.height,
            counter=current_counter,
            pos_x=current_pos_x,
            pos_y=current_pos_y
        )

        # Check for sprite position overflow in the X position
        if sprite_rect.pos_x + sprite_rect.width > MAX_WIDTH:
            sprite_rect.pos_x = 0
            sprite_rect.pos_y = 0

        # Check for collisions with existing sprites
        while any(rect.counter == sprite_rect.counter and rectangles_collided(sprite_rect, rect) for rect in organized_sprites):
            sprite_rect.pos_y += 1

        # Check for sprite position overflow in the Y position
        if sprite_rect.pos_y + sprite_rect.height > MAX_HEIGHT:
            sprite_rect.pos_x = sprite_rect.pos_y = 0
            sprite_rect.counter += 1

        organized_sprites.append(sprite_rect)

        current_pos_x = sprite_rect.pos_x
        current_pos_y = sprite_rect.pos_y
        current_counter = sprite_rect.counter

        current_pos_x += sprite_rect.width + 1
        current_pos_y = 0

    return organized_sprites

def pack_sprites(spritesheet: Image, sprite_positions: list[Rectangle]):
    """Pack the sprites into as many images as needed using the sprite position list."""
    current_counter = 0
    current_image = Image.new("RGBA", (MAX_WIDTH, MAX_HEIGHT))

    for sprite in sprite_positions:
        image_name = f"{BASE_IMAGE_NAME}{str(current_counter)}.png"

        sprite_image = spritesheet.crop((sprite.x, sprite.y, sprite.width + sprite.x, sprite.height + sprite.y))

        # Check if the sprite counter has changed, and if it does, save the image and create another one
        if current_counter != sprite.counter:
            current_image.save(image_name)
            current_counter = sprite.counter
            current_image = Image.new("RGBA", (MAX_WIDTH, MAX_HEIGHT))
            print(f"Packing sprite: {image_name}")

        # Check if the current sprite is the last one, and if it is, force saving the image to avoid bugs
        if sprite == sprite_positions[-1]:
            image_name = f"{BASE_IMAGE_NAME}{str(current_counter)}.png"
            current_image.paste(sprite_image, (sprite.pos_x, sprite.pos_y))
            current_image.save(image_name)
            print(f"Packing sprite: {image_name}")

        current_image.paste(sprite_image, (sprite.pos_x, sprite.pos_y))

def main():
    spritesheet_image = load_image(SPRITESHEET_FILE_PATH + ".png")
    sprite_xml = FNFXmlParser(scale=SCALE_FACTOR)
    sprite_xml.load(SPRITESHEET_FILE_PATH + ".xml")
    sprite_xml.parse_sprites_coordinates(ANIMATION_NAMES)

    if spritesheet_image.mode == "P":
        print("Warning: Image is indexed; converting to RGBA")
        spritesheet_image = spritesheet_image.convert(mode="RGBA")

    trimmed_sprite_attributes = get_sprites_coordinates(sprite_xml.sprites_coordinates, spritesheet_image)
    organized_sprite_positions = organize_sprite_positions(trimmed_sprite_attributes)
    pack_sprites(spritesheet_image, organized_sprite_positions)

if __name__ == "__main__":
    main()