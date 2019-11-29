class Shape:
    """
    Parent class of all shapes
    """


class Rectangle(Shape):
    """
    Makes SVG rectangles
    """

    def __init__(self):
        Shape.__init__(self)

    def __repr__(self):
        return f"Test"


