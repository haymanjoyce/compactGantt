# svg values need to be in double quotes

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


class Frame:

    def __init__(self, x=None, y=None, rx=None, ry=None, width=None, height=None,
                 fill=None, padding=None, border_color=None, border_width=None, margin=None):

        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.width = width
        self.height = height

    def __repr__(self):
        # need border because inner and outer rounding
        return f'<g transform="translate(100, 100)">' \
               f'<!--Margin--><rect x="0" y="0" width="200" height="200" fill="grey" fill-opacity="40"></rect>' \
               f'<!--Border--><rect x="20" y="20" width="160" height="160" fill="black"></rect>' \
               f'<!--Padding--><rect x="30" y="30" width="140" height="140" fill="green" fill-opacity="40""></rect>' \
               f'<!--Content--><rect x="40" y="40" width="120" height="120" fill="red" fill-opacity="40""></rect>' \
               f'</g>'

