# todo get rid of base class; switch from inheritance to composition
# todo switch to attrs; get rid of post_init; use attrs features like validation
# todo develop Scales with interface: placement, number of scales, grids to show
# todo make Interval class
# todo add order in as mixin to Scales
# todo add ability to label a scale to Scale
# todo use @property to render svg
# todo test other datetime libraries
# todo new mechanism for setting default date_format if blank
# todo add in attrs validator and default decorators
# todo use setters to change attributes that require other attributes to be updated

from attr import attrs, attrib
from shapes import Rectangle, Text
from labels import date_label


@attrs
class Scale:
    """Builds a scale feature"""

    # places the scale
    x = attrib(default=0)
    y = attrib(default=0)

    # time window dimensions
    width = attrib(default=800)
    height = attrib(default=600)

    # time window start and finish in ordinals
    start = attrib(default=0)  # note that ordinal dates are at 00:00hrs (day start)
    finish = attrib(default=0)  # we handle the missing 23:59 hours (you don't need to)

    # time window resolution (pixels per day)
    window_resolution = attrib(default=float())

    # defines first day of week as string
    week_start_text = attrib(default=str(0))

    # defines first day of week as integer
    week_start_num = attrib(default=0)

    # defines interval type
    interval_type = attrib(default=str())  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # private variable
    interval_data = attrib(default=tuple())

    # defines minimum interval width for a label
    min_interval_width = attrib(default=50)

    # defines label type
    label_type = attrib(default=str())  # count | hidden | date

    # defines date format
    date_format = attrib(default=str())  # y | yyyy | Y | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w | q | h

    # defines date format separator
    separator = attrib(default=" ")

    # interval styling
    box_rounding = attrib(default=0)
    box_border_width = attrib(default=0.2)
    box_border_color = attrib(default='black')
    box_fill = attrib(default='grey')

    # defines non-whole interval color
    scale_ends = attrib(default=str())

    # text styling
    font_fill = attrib(default='#000')
    font_size = attrib(default='20')  # 2em | smaller | etc.
    font_family = attrib(default=str())  # "Arial, Helvetica, sans-serif"
    font_style = attrib(default=str())  # normal | italic | oblique
    font_weight = attrib(default=str())  # normal | bold | bolder | lighter | <number>

    # text positioning relative to x and y
    text_x = attrib(default=None)
    text_y = attrib(default=None)

    def clean_bar_data(self):

        # clean date format separator
        if len(self.separator) < 1 or self.separator in ['%', '#', '?', '*', '\"'] or self.separator is self.separator.isdigit():
            self.separator = " "  # default

        # clean label type
        if self.label_type in ['HIDDEN', 'hidden', 'hide', 'h', None]:
            self.label_type = 'hidden'
        elif self.label_type in ['COUNT', 'count', 'c', '']:  # default if blank
            self.label_type = 'count'
        elif self.label_type in ['DATE', 'DATES', 'date', 'dates', 'd']:
            self.label_type = 'date'
        else:
            raise ValueError(self.label_type)

        # # set default date_format if blank
        # if self.label_type == 'date' and self.date_format == str():
        #     if self.interval_type == 'DAYS':
        #         self.date_format = 'a'
        #     elif self.interval_type == 'WEEKS':
        #         self.date_format = 'w'
        #     elif self.interval_type == 'MONTHS':
        #         self.date_format = 'mmm'
        #     elif self.interval_type == 'QUARTERS':
        #         self.date_format = 'q'
        #     elif self.interval_type == 'HALVES':
        #         self.date_format = 'h'
        #     elif self.interval_type == 'YEARS':
        #         self.date_format = 'yyyy'
        #     else:
        #         raise ValueError(self.interval_type)

        # set default text_x if None
        if self.text_x is None:
            self.text_x = 10  # arbitrary value

        # set default text_y if None
        if self.text_y is None:
            self.text_y = self.height * 0.65  # 0.65 sets text in middle

    def build_boxes(self):

        # set default scale end color if blank
        if self.scale_ends == str():
            self.scale_ends = self.box_fill

        # create Box object
        box = Rectangle()  # dropped Box class as internal bleed behaviour inconsistent with other SVG classes

        # create string for SVG
        boxes = str()

        # unchanging variables of Rect object
        box.y = self.y
        box.height = self.height
        box.border_rounding = self.box_rounding
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        # changing variables for Rect object
        for i in self.interval_data:
            box.x = i[0]
            box.width = i[1]
            if i[4] is False:
                box.fill_color = self.scale_ends
            else:
                box.fill_color = self.box_fill
            boxes += box.svg

        return boxes

    def build_labels(self):

        # create Text object
        label = Text()

        # create string for SVG
        labels = str()

        # unchanging variables for Text object
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

        # changing variables for Text object
        for i in self.interval_data:
            label.text_x = i[0]
            if i[1] < self.min_interval_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'count' and i[3] == 0:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'date':
                label.text = date_label(i[2], self.date_format, self.week_start_num, self.separator)
            else:
                label.text = i[3]  # references count in intervals entry
            labels += label.svg

        return labels

    def get_bar(self):

        self.clean_bar_data()

        return f'{self.build_boxes()} {self.build_labels()}'

    @property
    def svg(self):
        return self.get_bar()

