class Style:

    def __init__(self, fill=None, stroke=None, stroke_width=None, opacity=None):

        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.opacity = opacity

    def __repr__(self):
        return f'fill:{self.fill};' \
               f'stroke:{self.stroke};'


class Rectangle:

    def __init__(self, x=None, y=None, rx=None, ry=None, width=None, height=None, style=None):

        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.width = width
        self.height = height
        self.style = style

    def __repr__(self):
        return f'<rect width={self.width} ' \
               f'height={self.height} ' \
               f'style="{self.style}"></rect>'

