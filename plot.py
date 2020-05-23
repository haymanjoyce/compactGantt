# todo add svg property


from attr import attrs


@attrs
class Plot:
    """Objects represent the plot area"""

    x = 0.0
    y = 0.0

    width = 800.0
    height = 600.0

    start = 0  # note that ordinal dates are at day start (00:00hrs)
    finish = 0

    pixels_per_day = 1.0

    def __attrs_post_init__(self):
        self.clean_dates()
        self.pixels_per_day = self.get_pixels_per_day()

    def clean_dates(self):
        if self.finish <= self.start:
            self.finish = self.start + 1

    def get_pixels_per_day(self):
        return self.width / ((self.finish + 1) - self.start)  # finish is day end (23:59hrs)

