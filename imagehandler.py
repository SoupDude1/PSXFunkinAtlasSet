from PIL import Image
from util import Rectangle, rectangles_collided

# Max image size
MAX_WIDTH = 256
MAX_HEIGHT = 256

class ImageHandler:
    def __init__(self, image_name):
        self.sprite_coordinates: list[Rectangle] = []
        self.organized_sprites: list[Rectangle] = []

        self.image_name = image_name
        self.spritesheet = None

    def load(self, path: str) -> Image.Image:
        """Load a PNG file and return it."""
        png_file = Image.open(path)
        print(f"Loading {path}...")
        print("Loaded!")

        if png_file.mode == "P":
            print(f"Warning: Image is indexed; converting to RGBA")
            png_file = png_file.convert(mode="RGBA")

        return png_file

    def load_spritesheet(self, path: str) -> Image.Image:
        """Load the PNG spritesheet."""
        self.spritesheet = self.load(path)

        return self.spritesheet

    def get_sprites_coordinates(self, xml_attributes: list[Rectangle]):
        """Generate a list of non empty space sprite coordinates from the XML list."""
        for attribute in xml_attributes:
            sprite = self._crop_spritesheet(attribute)
            adjusted_sprite = self._remove_empty_space_from_sprite(sprite, attribute)
            self.sprite_coordinates.append(adjusted_sprite)

    def organize_sprites_positions(self):
        """Organize sprite positions for efficient packing."""
        current_pos_x = 0
        current_pos_y = 0
        current_counter = 0

        for i in self.sprite_coordinates:
            sprite_rect = Rectangle(
                x=i.x,
                y=i.y,
                width=i.width,
                height=i.height,
                counter=current_counter,
                pos_x=current_pos_x,
                pos_y=current_pos_y
            )

            if sprite_rect.pos_x + sprite_rect.width > MAX_WIDTH:
                sprite_rect.pos_x = 0
                sprite_rect.pos_y = 0

            while any(rect.counter == sprite_rect.counter and rectangles_collided(sprite_rect, rect) for rect in self.organized_sprites):
                sprite_rect.pos_y += 1

            if sprite_rect.pos_y + sprite_rect.height > MAX_HEIGHT:
                sprite_rect.pos_x = sprite_rect.pos_y = 0
                sprite_rect.counter += 1

            self.organized_sprites.append(sprite_rect)

            current_pos_x = sprite_rect.pos_x
            current_pos_y = sprite_rect.pos_y
            current_counter = sprite_rect.counter

            current_pos_x += sprite_rect.width + 1
            current_pos_y = 0

    def pack_sprites(self):
        """Pack the sprites into images."""
        current_counter = 0
        current_image = Image.new("RGBA", (MAX_WIDTH, MAX_HEIGHT))

        for sprite in self.organized_sprites:
            image_name = f"{self.image_name}{str(current_counter)}.png"
            sprite_image = self._crop_spritesheet(sprite)

            if current_counter != sprite.counter:
                current_image.save(image_name)
                current_counter = sprite.counter
                current_image = Image.new("RGBA", (MAX_WIDTH, MAX_HEIGHT))
                print(f"Packing sprite: {image_name}")

            if sprite == self.sprite_coordinates[-1]:
                image_name = f"{self.image_name}{str(current_counter)}.png"
                current_image.paste(sprite_image, (sprite.pos_x, sprite.pos_y))
                current_image.save(image_name)
                print(f"Packing sprite: {image_name}")

            current_image.paste(sprite_image, (sprite.pos_x, sprite.pos_y))

    def _crop_spritesheet(self, sprite_rect : Rectangle):
        if self.spritesheet is None:
            raise TypeError("Failed to crop spritesheet")

        return self.spritesheet.crop((sprite_rect.x, sprite_rect.y, sprite_rect.width + sprite_rect.x, sprite_rect.height + sprite_rect.y))

    def _remove_empty_space_from_sprite(self, sprite_image, sprite_rect: Rectangle) -> Rectangle:
        """Remove empty space from the given sprite."""
        if sprite_image.getbbox() is None:
            raise TypeError("Failed to pack sprites; check for empty sprite spaces or correct XML scale")

        bbox = sprite_image.getbbox()

        adjusted_sprite = Rectangle(
            x=sprite_rect.x + bbox[0],
            y=sprite_rect.y + bbox[1],
            width=bbox[2] - bbox[0],
            height=bbox[3] - bbox[1]
        )

        return adjusted_sprite