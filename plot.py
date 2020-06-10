# todo check resolution calculation
# todo improve attribute management

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
    resolution = 1.0  # pixels per day

    def clean_dates(self):
        if self.finish <= self.start:
            self.finish = self.start + 1

    def calculate_resolution(self):
        self.resolution = self.width / (self.finish - self.start)  # finish is day end (23:59hrs)

