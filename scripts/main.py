from xmlparser import XmlParser
from imagehandler import ImageHandler

# Path to the spritesheet file
SPRITESHEET_FILE_PATH = "example/BOYFRIEND"
# Base name for sprite image files
BASE_IMAGE_NAME = "bf"
# Scaling factor to resize the sprites
SCALE_FACTOR = 0.25

# Bits per pixel of the image
BPP = 4

# Names of animations to be extracted from the XML file
ANIMATION_NAMES = ["BF idle dance", "BF NOTE LEFT", "BF NOTE DOWN", "BF NOTE UP", "BF NOTE RIGHT"]
ANIMATION_OFFSETS = [(-5, 0), (5, -6), (-20, -51), (-46, 27), (-48, -7)]

def main():
    sprite_xml = XmlParser(scale=SCALE_FACTOR)
    sprite_xml.load(SPRITESHEET_FILE_PATH + ".xml")
    sprite_xml.parse_sprites_coordinates(ANIMATION_NAMES, ANIMATION_OFFSETS)

    sprite_png = ImageHandler(image_name=BASE_IMAGE_NAME, bpp=BPP)
    sprite_png.load(SPRITESHEET_FILE_PATH + ".png")
    sprite_png.get_sprites_coordinates(sprite_xml.sprites_coordinates)
    sprite_png.organize_sprites_positions()
    sprite_png.pack_sprites()

    with open(bf + ".h", "w") as f:
        for i in sprite_png.organized_sprites:
            f.write(f"{{{i.counter}, {{{i.pos_x}, {i.pos_y}, {i.width}, {i.height}}}")
            f.write(f", {{{i.offset_x}, {i.offset_y}}}}}, \n")

if __name__ == "__main__":
    main()