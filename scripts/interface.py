import flet as ft
from xmlparser import XmlParser
from imagehandler import ImageHandler
from util import ErrorScreen

# Constants
BPP = 8
ANIMATION_NAMES = ["BF idle dance", "BF NOTE LEFT", "BF NOTE DOWN", "BF NOTE UP", "BF NOTE RIGHT"]
ANIMATION_OFFSETS = [(-5, 0), (5, -6), (-20, -51), (-46, 27), (-48, -7)]

class TextFieldWidget(ft.UserControl):
    def __init__(self, text: str, hint_text: str) -> None:
        super().__init__()
        self.text = text
        self.hint_text = hint_text
        self.widget = ft.TextField(
            label=self.text,
            hint_text=self.hint_text,
            border_radius=ft.border_radius.all(15),
            label_style=ft.TextStyle(font_family="Open Sans"),
            text_style=ft.TextStyle(font_family="Open Sans")
        )

    def build(self) -> ft.TextField:
        return self.widget


class DropdownWidget(ft.UserControl):
    def __init__(self, options : list[str], page) -> None:
        super().__init__()
        self.options = options
        self.widget = ft.Dropdown(options=[ ft.dropdown.Option("Why")])
        self.page = page

    def build(self) -> ft.Dropdown:
        return self.widget

    def add_option(self, text, page) -> None:
        if not any(i.key == text for i in self.widget.options):
            self.widget.options.append(ft.dropdown.Option(text))
            self.widget.value = text
            page()

def interface(page: ft.Page):
    # Set the title and theme mode
    page.title = "PSXFunkinAtlasSet 0.1"
    page.theme_mode = ft.ThemeMode.DARK

    # Define fonts
    page.fonts = {
        "Open Sans": "https://github.com/google/fonts/raw/main/apache/opensanshebrew/OpenSansHebrew-Regular.ttf"
    }

    ErrorScreen.get_page(page)

    def change_tab(e):
        current_index = page.navigation_bar.content.selected_index
        char_options.visible = current_index == 0
        page.update()

    def load_character(e):
        sprite_xml = XmlParser(scale=character_scale.widget.value)
        sprite_xml.load(character_path.widget.value + ".xml")
        sprite_xml.parse_sprites_coordinates(ANIMATION_NAMES, ANIMATION_OFFSETS)

        sprite_png = ImageHandler(image_name=character_name.widget.value, bpp=BPP)
        sprite_png.load(character_path.widget.value + ".png")
        sprite_png.get_sprites_coordinates(sprite_xml.sprites_coordinates)
        sprite_png.organize_sprites_positions()
        sprite_png.pack_sprites()

    # Create the navigation bar
    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon="image", label="Assets"),
                ft.NavigationDestination(icon="animation", label="Animation"),
                ft.NavigationDestination(icon="gamepad", label="Playstation"),
            ],
            bgcolor="blue800",
            on_change=change_tab,
        ),
        border_radius=ft.border_radius.all(15),
    )

    # Create text input widgets
    character_path = TextFieldWidget("Character path", "example/BOYFRIEND")
    character_name = TextFieldWidget("Character name", "example/bf")
    character_scale = TextFieldWidget("Scale factor", "0.25")

    animations = DropdownWidget([], page)

    animation_text = TextFieldWidget("Animation name", "Idle Dance")

    add_animation = ft.OutlinedButton(icon="add", text="Add Animation", on_click=lambda e: animations.add_option(animation_text.widget.value, page.update))

    # Create the "Generate" button
    submit = ft.OutlinedButton(icon="send", text="Generate", on_click=load_character)

    # Create a container for character options
    char_options = ft.Container(
        content=ft.Column(controls=[character_path, character_name, character_scale, submit, animations, animation_text, add_animation]),
        width=200,
    )

    page.add(char_options)
