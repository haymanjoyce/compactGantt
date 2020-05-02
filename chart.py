"""Classes for building the SVG"""

# todo develop Layout and features
# todo render main boxes which other modules render in more detail
# todo remove viewbox attributes from svg element

from dataclasses import dataclass


@dataclass
class Chart:
    """Handles image and creates images of chart in various formats"""

    chart: str = str()

    viewPort_width: int = 800
    viewPort_height: int = 600

    viewBox_x: int = -100
    viewBox_y: int = -100

    viewBox_width: int = 1600
    viewBox_height: int = 1200

    def get_svg(self):
        return f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'viewBox="{self.viewBox_x} {self.viewBox_y} {self.viewBox_width} {self.viewBox_height}" ' \
               f'id="" overflow="auto"> ' \
               f'{self.chart}' \
               f'</svg>'

