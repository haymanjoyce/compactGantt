# todo add ability to prefix date format (e.g. Week 2, Q2, Half 2) (replaces Q, H, and Y)

from attr import attrs, attrib
from datetime import date


@attrs
class Date:

    ordinal_date = attrib(default=date.toordinal(date.today()))
    date_format = attrib(default='dd mmm yyyy')
    _week_start = attrib(default=0)
    _separator = attrib(default=' ')

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

    def custom_format(self):
        """Converts an ordinal date into a custom date format"""

        # y - 20
        # Y - Y20
        # yyyy - 2020
        # m - 4
        # mm - 04
        # mmm - Apr
        # M - April
        # d - 6
        # dd - 06
        # a - M
        # aaa - Mon
        # A - Monday
        # n - 97 (day of the year as number where 1 Jan is day 1)
        # nnn - 097 (day of the year as number where 1 Jan is day 1)
        # w - 14 (week number where week_start argument determines weeks commencing Mon or Sun)
        # q - 2
        # Q - Q2
        # h - 1
        # H = H1

        if self.week_start not in [0, 6]:  # Python only handles Mondays or Sundays
            self.week_start = 0

        dt = date.fromordinal(self.ordinal_date)

        day = dt.day
        month = dt.month

        items = str(self.date_format).strip().split()

        label = str()

        for item in items:

            if "y".upper() in item.upper():
                if item == "y":
                    label += dt.strftime("%y")
                elif item == "Y":
                    label += "Y" + dt.strftime("%y")
                else:
                    label += dt.strftime("%Y")
            elif "m".upper() in item.upper():
                if item == "m":
                    label += str(month)
                elif item == "mm":
                    label += dt.strftime("%m")
                elif item == "mmm":
                    label += dt.strftime("%b")
                else:
                    label += dt.strftime("%B")
            elif "d".upper() in item.upper():
                if item == "d":
                    label += str(day)
                else:
                    label += dt.strftime("%d")
            elif "a".upper() in item.upper():
                if item in ["a", "aa"]:
                    label += dt.strftime("%a")[0]
                elif item == "aaa":
                    label += dt.strftime("%a")
                else:
                    label += dt.strftime("%A")
            elif "n".upper() in item.upper():
                if item in ["n", "nn"]:
                    label += str(dt.timetuple()[7])
                else:
                    label += dt.strftime("%j")
            elif "w".upper() in item.upper():
                if self.week_start == 0:
                    label += dt.strftime("%W")
                else:
                    label += dt.strftime("%U")
            elif "q".upper() in item.upper():
                if "Q" in item:
                    label += 'Q' + str(find_quarter(month))
                else:
                    label += str(find_quarter(month))
            elif "h".upper() in item.upper():
                if "H" in item:
                    label += 'H' + str(find_half(month))
                else:
                    label += str(find_half(month))
            else:
                raise ValueError(item)

            label += " "

        return label.strip().replace(" ", str(self.separator))


def find_quarter(month):
    """Converts month number into quarter number (Python does not have a builtin)"""

    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    elif month in [10, 11, 12]:
        return 4
    else:
        raise ValueError(month)


def find_half(month):
    """Converts month number into half number (Python does not have a builtin)"""

    if month in [1, 2, 3, 4, 5, 6]:
        return 1
    elif month in [7, 8, 9, 10, 11, 12]:
        return 2
    else:
        raise ValueError(month)

