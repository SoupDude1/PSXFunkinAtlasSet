class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0, counter=0, pos_x=0, pos_y=0):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.counter: int = counter
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y

def rectangles_are_equal(rect1: Rectangle, rect2: Rectangle) -> bool:
    """Check if both rectangles have the same values for the members 'x, y, width, and height'."""
    return all(getattr(rect1, attr) == getattr(rect2, attr) for attr in ["x", "y", "width", "height"])

def rectangles_collided(rect1: Rectangle, rect2: Rectangle) -> bool:
    """Check if 2 rectangles have collided."""
    return (rect1.pos_x < rect2.pos_x + rect2.width and rect1.pos_x + rect1.width > rect2.pos_x and
            rect1.pos_y < rect2.pos_y + rect2.height and rect1.pos_y + rect1.height > rect2.pos_y)

