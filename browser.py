from attr import attrs, attrib
import os


@attrs
class Browser:
    """Creates or updates HTML file, which contains SVG image"""

    image = str()
    location = attrib()
    filename = attrib(default='page.html')

    @location.default
    def get_location(self):
        return os.path.dirname(str(__file__))

    def update_page(self):
        filepath = os.path.join(self.location, self.filename)
        file = open(filepath, "w")
        file.write(self.wrap_image())
        file.close()

    def wrap_image(self):
        return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>{self.image}</body></html>'


browser = Browser()


def display_chart(svg='<p>No SVG code found.</p>'):
    """Public interface to Browser"""
    browser.image = svg
    browser.update_page()

