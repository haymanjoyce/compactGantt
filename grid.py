from attr import attrs, attrib
from shapes import Line
from intervals import Intervals


@attrs
class Grid:
    """Builds a grid feature"""

    x = attrib(default=0)
    y = attrib(default=0)
    width = attrib(default=800)
    height = attrib(default=600)
    start = attrib(default=0)  # note that ordinal dates are at 00:00hrs (day start)
    finish = attrib(default=0)  # we handle the missing 23:59 hours (you don't need to)
    resolution = attrib(default=float())
    interval_data = attrib(default=tuple())
    interval_type = attrib(default='DAYS')
    week_start = attrib(default=0)
    line_color: str = 'black'
    line_width: int = 1
    line_dashing: str = str()  # dash gap dash gap

    def build_grid(self):

        intervals = Intervals()
        intervals.interval_type = self.interval_type
        intervals.x = self.x
        intervals.start = self.start
        intervals.finish = self.finish
        intervals.resolution = self.resolution
        intervals.week_start = self.week_start

        line = Line()
        line.y = self.y
        line.dy = self.y + self.height
        line.stroke_color = self.line_color
        line.stroke_width = self.line_width
        line.stroke_dasharray = self.line_dashing

        lines = str()

        for i in intervals.get_intervals():
            line.x = i[0]
            line.dx = line.x
            lines += line.svg

        last_line = self.x + ((self.finish - self.start) * self.resolution)
        line.x = last_line
        line.dx = last_line
        lines += line.svg

        return lines

    @property
    def svg(self):

        return f'{self.build_grid()}'

