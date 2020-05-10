from attr import attrs, attrib
import os


@attrs
class Browser:

    image = str()
    location = attrib()
    filename = attrib(default='page.html')

    @location.default
    def get_location(self):
        return os.path.dirname(str(__file__))

    def update_page(self):
        filepath = os.path.join(self.location, self.filename)
        file = open(filepath, "w")
        file.write(self.parse_page())
        file.close()

    def parse_page(self):
        return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>{self.image}</body></html>'


browser = Browser()


def display_chart(svg='<p>No SVG code found.</p>'):
    browser.image = svg
    browser.update_page()

