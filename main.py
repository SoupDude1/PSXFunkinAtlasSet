from xmlparser import XmlParser
from imagehandler import ImageHandler

# Path to the spritesheet file
SPRITESHEET_FILE_PATH = "example/BOYFRIEND"
# Base name for sprite image files
BASE_IMAGE_NAME = "bf"
# Scaling factor to resize the sprites
SCALE_FACTOR = 0.25

# Names of animations to be extracted from the XML file
ANIMATION_NAMES = ["BF idle dance", "BF NOTE LEFT", "BF NOTE DOWN", "BF NOTE UP", "BF NOTE RIGHT"]

def main():
    sprite_xml = XmlParser(scale=SCALE_FACTOR)
    sprite_xml.load(SPRITESHEET_FILE_PATH + ".xml")
    sprite_xml.parse_sprites_coordinates(ANIMATION_NAMES)

    sprite_png = ImageHandler(image_name=BASE_IMAGE_NAME)
    sprite_png.load_spritesheet(SPRITESHEET_FILE_PATH + ".png")
    sprite_png.get_sprites_coordinates(sprite_xml.sprites_coordinates)
    sprite_png.organize_sprites_positions()
    sprite_png.pack_sprites()

if __name__ == "__main__":
    main()