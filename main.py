import xml.etree.ElementTree as ET
from PIL import Image
from util import *

# Path to the spritesheet file
SPRITESHEET_FILE_PATH = "example/BOYFRIEND"
# Base name for sprite image files
BASE_IMAGE_NAME = "bf"
# Scaling factor to resize the sprites
SCALE_FACTOR = 0.25

# Names of animations to be extracted from the XML file
ANIMATION_NAMES = ["BF idle dance", "BF NOTE LEFT", "BF NOTE DOWN", "BF NOTE UP", "BF NOTE RIGHT"]

# Function to load an image from a file
def load_image(file_path):
    try:
        print(f"Loading {file_path}...")
        print(f"Loaded!")
        return Image.open(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Failed to load {file_path}")

# Function to load XML data from a file
def load_xml(file_path):
    try:
        print(f"Loading {file_path}...")
        print(f"Loaded!")
        return ET.parse(file_path).getroot()

    except FileNotFoundError:
        raise FileNotFoundError(f"Failed to load {file_path}")

# Extract the FNF sprite sheet XML attributes and scale their properties as needed
def extract_sprite_attributes(xml_data):
    sprite_attributes = []

    for animation_name in ANIMATION_NAMES:
        for sub_texture in xml_data.findall("SubTexture"):
            if not compare_strings_ignore_trailing_numbers(animation_name, sub_texture.get("name")):
                continue

            # Create a sprite rectangle and scale its attributes if needed
            sprite_rect = Rectangle(
                x=custom_round(int(sub_texture.get("x")) * SCALE_FACTOR),
                y=custom_round(int(sub_texture.get("y")) * SCALE_FACTOR),
                width=custom_round(int(sub_texture.get("width")) * SCALE_FACTOR),
                height=custom_round(int(sub_texture.get("height")) * SCALE_FACTOR)
            )

            # Check if the same frame exists in the XML list before appending
            if not any(are_sprite_rectangles_equal(sprite_rect, existing_rect) for existing_rect in sprite_attributes):
                sprite_attributes.append(sprite_rect)

    return sprite_attributes

# Function to trim sprites based on their attributes
def trim_sprites(sprite_attributes, spritesheet):
    trimmed_sprites = []

    for sprite_attr in sprite_attributes:
        sprite = spritesheet.crop((sprite_attr.x, sprite_attr.y, sprite_attr.width + sprite_attr.x, sprite_attr.height + sprite_attr.y))

        # Check if the sprite has valid content
        if sprite.getbbox() is None:
            raise TypeError("Failed to pack sprites, check if your spritesheet has empty sprite spaces or if the XML scale is correct")

        bbox = sprite.getbbox()

        # Create a trimmed sprite rectangle
        trimmed_sprite_rect = Rectangle(
            x=sprite_attr.x + bbox[0],
            y=sprite_attr.y + bbox[1],
            width=bbox[2] - bbox[0],
            height=bbox[3] - bbox[1]
        )

        trimmed_sprites.append(trimmed_sprite_rect)

    return trimmed_sprites

# Function to organize sprite positions for multiples images
def organize_sprite_positions(trimmed_sprites):
    sprite_positions = []
    current_pos_x = 0
    current_pos_y = 0
    current_counter = 0

    for trimmed_sprite in trimmed_sprites:
        # Create a sprite position rectangle
        sprite_position = Rectangle(
            x=trimmed_sprite.x,
            y=trimmed_sprite.y,
            width=trimmed_sprite.width,
            height=trimmed_sprite.height,
            counter=current_counter,
            pos_x=current_pos_x,
            pos_y=current_pos_y
        )

        collided = False

        # Check for sprite position overflow in the X position
        if sprite_position.pos_x + sprite_position.width > 256:
            sprite_position.pos_x = 0
            sprite_position.pos_y = 0

        # Check for collisions with existing sprites
        while any(rect.counter == sprite_position.counter and do_sprite_rectangles_collide(sprite_position, rect) for rect in sprite_positions):
            sprite_position.pos_y += 1
            collided = True

        if collided:
            sprite_position.pos_y += 1

        # Check for sprite position overflow in the Y position
        if sprite_position.pos_y + sprite_position.height > 256:
            sprite_position.pos_x = sprite_position.pos_y = 0
            sprite_position.counter += 1

        sprite_positions.append(sprite_position)

        current_pos_x = sprite_position.pos_x
        current_pos_y = sprite_position.pos_y
        current_counter = sprite_position.counter

        current_pos_x += sprite_position.width + 1
        current_pos_y = 0

    return sprite_positions

# Function to pack sprites into multiples images or only a single one
def pack_sprites(spritesheet, sprite_positions):
    current_counter = 0
    current_image = Image.new("RGBA", (256, 256))

    for sprite_position in sprite_positions:
        image_name = f"{BASE_IMAGE_NAME}{str(current_counter)}.png"

        sprite = spritesheet.crop((sprite_position.x, sprite_position.y, sprite_position.width + sprite_position.x, sprite_position.height + sprite_position.y))

        # Check if the sprite counter has changed
        if current_counter != sprite_position.counter:
            current_image.save(image_name)
            current_counter = sprite_position.counter
            current_image = Image.new("RGBA", (256, 256))
            print(f"Packing sprite: {image_name}")

        # Check if the current sprite is the last one
        if sprite_position == sprite_positions[-1]:
            image_name = f"{BASE_IMAGE_NAME}{str(current_counter)}.png"
            current_image.paste(sprite, (sprite_position.pos_x, sprite_position.pos_y))
            current_image.save(image_name)
            print(f"Packing sprite: {image_name}")

        current_image.paste(sprite, (sprite_position.pos_x, sprite_position.pos_y))

if __name__ == "__main__":
    spritesheet_image = load_image(SPRITESHEET_FILE_PATH + ".png")

    if spritesheet_image.mode == "P":
        print("Warning: Image is indexed; converting to RGBA")
        spritesheet_image = spritesheet_image.convert(mode="RGBA")

    xml_data = load_xml(SPRITESHEET_FILE_PATH + ".xml")
    sprite_attributes_list = extract_sprite_attributes(xml_data)
    trimmed_sprite_attributes = trim_sprites(sprite_attributes_list, spritesheet_image)
    organized_sprite_positions = organize_sprite_positions(trimmed_sprite_attributes)
    pack_sprites(spritesheet_image, organized_sprite_positions)