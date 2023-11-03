from dataclasses import dataclass
import flet as ft

@dataclass
class Rectangle:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    counter: int = 0
    pos_x: int = 0
    pos_y: int = 0

def rectangles_are_equal(rect1: Rectangle, rect2: Rectangle) -> bool:
    """Check if both rectangles have the same values for the members 'x, y, width, and height'."""
    return all(getattr(rect1, attr) == getattr(rect2, attr) for attr in ["x", "y", "width", "height"])

def rectangles_collided(rect1: Rectangle, rect2: Rectangle) -> bool:
    """Check if 2 rectangles have collided."""
    return (rect1.pos_x < rect2.pos_x + rect2.width and rect1.pos_x + rect1.width > rect2.pos_x and
            rect1.pos_y < rect2.pos_y + rect2.height and rect1.pos_y + rect1.height > rect2.pos_y)


# I am putting this here to avoid circular import issue
class ErrorScreen(ft.UserControl):
    error_message = ""
    page = None
    banner = ft.Banner(
        bgcolor="grey600",
        leading=ft.Icon("warning", color="red", size=40),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: ErrorScreen._close_banner()),
        ],
    )

    @classmethod
    def message(cls, message) -> None:
        cls.error_message = message
        cls.page.banner = cls.get_banner()
        cls.banner.content = ft.Text(cls.error_message)
        cls.page.banner.open = True
        cls.page.update()
        raise Exception("Banner Error found!")

    @classmethod
    def get_banner(cls) -> ft.Banner:
        return cls.banner

    @classmethod
    def get_page(cls, page) -> None:
        cls.page = page

    @classmethod
    def _close_banner(cls):
        cls.page.banner.open = False
        cls.page.update()


