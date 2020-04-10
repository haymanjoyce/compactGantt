"""Module for assembling chart features"""

# todo possible Scales class for building multiple scales with one interface

from dataclasses import dataclass


@dataclass
class Item:
    """
    Creates tuple of metadata and SVG string
    Did not make sense to make this parent of shape class
    Sometimes multiple shapes are grouped and it is the grouped element that we want to apply this class to
    """

    layer: int = 100
    element: str = str()

    def get_item(self):
        return self.layer, self.element

