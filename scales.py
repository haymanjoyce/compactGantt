# todo make box, text, interval and date objects components

from attr import attrs, attrib
from shapes import Rectangle, Text
from dates import Date


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

    interval_data = attrib(default=tuple())

    min_label_width = attrib(default=50)

    _label_type = attrib(default='date')  # count | hidden | date

    _ends = attrib(default=str())

    date_format = attrib(default=str())  # y | yyyy | Y | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w | q | h
    separator = attrib(default=" ")
    week_start = attrib(default=0)

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
    def ends(self):
        if self._ends == str():
            return self.box_fill
        else:
            return self._ends

    @ends.setter
    def ends(self, color):
        self._ends = color

    def build_boxes(self):

        box = Rectangle()
        boxes = str()

        box.y = self.y
        box.height = self.height
        box.border_rounding = self.box_rounding
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        for i in self.interval_data:
            box.x = i[0]
            box.width = i[1]
            if i[4] is False:
                box.fill_color = self.ends
            else:
                box.fill_color = self.box_fill
            boxes += box.svg

        return boxes

    def build_labels(self):

        date = Date()
        date.week_start = self.week_start
        date.separator = self.separator
        date.date_format = self.date_format

        label = Text()
        labels = str()

        label.text_y = self.y
        label.text_translate_y = self.text_y
        label.text_translate_x = self.text_x
        label.font_fill_color = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        if self.label_type == 'hidden':
            label.text_visibility = 'hidden'

        for i in self.interval_data:
            label.text_x = i[0]
            if i[1] < self.min_label_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'count' and i[3] == 0:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'date':
                date.ordinal_date = i[2]
                label.text = date.custom_format()
            else:
                label.text = i[3]  # references count in intervals entry
            labels += label.svg

        return labels

    @property
    def svg(self):

        # update calculated fields here

        return f'{self.build_boxes()} {self.build_labels()}'

