from xmlparser import XmlParser
from imagehandler import ImageHandler
from interface import interface

import flet as ft

# Names of animations to be extracted from the XML file
ANIMATION_NAMES = ["idle", "left", "down", "up", "right"]
ANIMATION_OFFSETS = [(-5, 0), (5, -6), (-20, -51), (-46, 27), (-48, -7)]

def main():
    ft.app(target=interface)

    # with open(BASE_IMAGE_NAME + ".h", "w") as f:
    #     for i in sprite_png.organized_sprites:
    #         f.write(f"{{{i.counter}, {{{i.pos_x}, {i.pos_y}, {i.width}, {i.height}}}")
    #         f.write(f", {{{i.offset_x}, {i.offset_y}}}}}, \n")

if __name__ == "__main__":
    main()