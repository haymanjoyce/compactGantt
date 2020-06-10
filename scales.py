# todo clean data elsewhere

from attr import attrs, attrib
from dates import Date
from intervals import Intervals
from shapes import Rectangle, Text


@attrs
class Scale:
    """Builds a scale feature"""

    x = attrib(default=0)
    y = attrib(default=0)

    width = attrib(default=800)
    height = attrib(default=600)

    start = attrib(default=0)  # note that ordinal dates are at 00:00hrs (day start)
    finish = attrib(default=0)  # we handle the missing 23:59 hours (you don't need to)

    resolution = attrib(default=float())

    min_label_width = attrib(default=50)

    date_format = attrib(default=str())  # y | yyyy | Y | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w | q | h

    box_rounding = attrib(default=0)
    box_border_width = attrib(default=0.2)
    box_border_color = attrib(default='black')
    box_fill = attrib(default='grey')

    font_fill = attrib(default='#000')
    font_size = attrib(default='20')  # 2em | smaller | etc.
    font_family = attrib(default=str())  # "Arial, Helvetica, sans-serif"
    font_style = attrib(default=str())  # normal | italic | oblique
    font_weight = attrib(default=str())  # normal | bold | bolder | lighter | <number>

    text_x = attrib(default=0)
    text_y = attrib(default=0)

    _interval_type = attrib(default='DAYS')

    _label_type = attrib(default='date')  # count | hidden | date

    _ends = attrib(default=str())

    _week_start = attrib(default=0)

    _separator = attrib(default=" ")

    @property
    def ends(self):
        if self._ends == str():
            return self.box_fill
        else:
            return self._ends

    @ends.setter
    def ends(self, color):
        self._ends = color

    @property
    def label_type(self):
        return self._label_type

    @label_type.setter
    def label_type(self, value):
        value = str(value).lower()
        if value in ['hidden', 'hide', 'h', 'none']:
            self._label_type = 'hidden'
        elif value in ['count', 'c', '']:  # default if blank
            self._label_type = 'count'
        elif value in ['date', 'dates', 'd']:
            self._label_type = 'date'
        else:
            raise ValueError(value)

    @property
    def interval_type(self):
        return self._interval_type

    @interval_type.setter
    def interval_type(self, value):
        value = str(value).lower()
        if value in ['days', 'day', 'd', '']:
            self._interval_type = 'DAYS'
        elif value in ['weeks', 'week', 'wk', 'w']:
            self._interval_type = 'WEEKS'
        elif value in ['months', 'mon', 'month', 'm']:
            self._interval_type = 'MONTHS'
        elif value in ['quarters', 'quarts', 'qts', 'q']:
            self._interval_type = 'QUARTERS'
        elif value in ['halves', 'half', 'halfs', 'halve', 'h']:
            self._interval_type = 'HALVES'
        elif value in ['years', 'year', 'yrs', 'yr', 'y']:
            self._interval_type = 'YEARS'
        else:
            raise ValueError(value)

    @property
    def week_start(self):
        return self._week_start

    @week_start.setter
    def week_start(self, value):
        value = str(value)
        if value in ['6', '7', 'S', 'Sun', 'Sunday']:
            self._week_start = 6
        else:
            self._week_start = 0

    @property
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, value):
        value = str(value)
        if len(value) > 1 or value in ['%', '#', '?', '*', '\"']:
            self._separator = '-'
        else:
            self._separator = value

    def build_boxes(self):

        intervals = Intervals()
        intervals.interval_type = self.interval_type
        intervals.x = self.x
        intervals.start = self.start
        intervals.finish = self.finish
        intervals.resolution = self.resolution
        intervals.week_start = self.week_start

        box = Rectangle()
        box.y = self.y
        box.height = self.height
        box.border_rounding = self.box_rounding
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        boxes = str()

        for i in intervals.get_intervals():
            box.x = i[0]
            box.width = i[1]
            if i[4] is False:
                box.fill_color = self.ends
            else:
                box.fill_color = self.box_fill
            boxes += box.svg

        return boxes

    def build_labels(self):

        intervals = Intervals()
        intervals.interval_type = self.interval_type
        intervals.x = self.x
        intervals.start = self.start
        intervals.finish = self.finish
        intervals.resolution = self.resolution
        intervals.week_start = self.week_start

        date = Date()
        date.week_start = self.week_start
        date.separator = self.separator
        date.date_format = self.date_format

        label = Text()
        label.text_y = self.y
        label.text_translate_y = self.text_y
        label.text_translate_x = self.text_x
        label.font_fill_color = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        labels = str()

        if self.label_type == 'hidden':
            label.text_visibility = 'hidden'

        for i in intervals.get_intervals():
            label.text_x = i[0]
            if i[1] < self.min_label_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'count' and i[3] == 0:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'date':
                date.ordinal_date = i[2]
                label.text = date.get_date()
            else:
                label.text = i[3]  # references count in intervals entry
            labels += label.svg

        return labels

    @property
    def svg(self):

        return f'{self.build_boxes()} {self.build_labels()}'

