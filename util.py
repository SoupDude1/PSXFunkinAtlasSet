import re

class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0, counter=0, pos_x=0, pos_y=0):
        self.x : int = x
        self.y : int = y
        self.width : int = width
        self.height : int = height
        self.counter : int = counter
        self.pos_x : int = pos_x
        self.pos_y : int = pos_y

def rectangles_are_equal(rect1 : Rectangle, rect2 : Rectangle) -> bool:
    return all(getattr(rect1, attr) == getattr(rect2, attr) for attr in ["x", "y", "width", "height"])

def rectangles_collided(rect1 : Rectangle, rect2 : Rectangle) -> bool:
    return (rect1.pos_x < rect2.pos_x + rect2.width and rect1.pos_x + rect1.width > rect2.pos_x and
            rect1.pos_y < rect2.pos_y + rect2.height and rect1.pos_y + rect1.height > rect2.pos_y)

def custom_round(value : float):
    if value >= 0:
        return int(value + 0.5)
    else:
        return int(value - 0.5)

def compare_strings_ignore_trailing_numbers(str1 : str, str2 : str):
    str1_stripped = re.sub(r"\d+$", "", str1)
    str2_stripped = re.sub(r"\d+$", "", str2)
    return str1_stripped == str2_stripped