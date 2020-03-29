"""Module for handling dates"""

# todo clean separator (e.g. only one or two chars or forbidden chars)
# todo restrict week start to Mon or Sun (boolean) because no week labels for other cases in Python
# todo ability to prefix date format (e.g. Week 2)
# todo improve speed (e.g. by making it class)
# todo label for quarters and halves

import datetime as dt


def convert_ordinal(ordinal_date, date_format, week_start=0, separator=' '):
    """Converts ordinal date into custom date format"""

    # y - 20
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

    if week_start not in [0, 6]:
        raise ValueError(week_start)

    date = dt.date.fromordinal(ordinal_date)
    items = str(date_format).strip().split()
    label = str()

    for item in items:

        if "y".upper() in item.upper():
            if item == "y":
                label += date.strftime("%y")
            else:
                label += date.strftime("%Y")
        elif "m".upper() in item.upper():
            if item == "m":
                label += str(date.month)
            elif item == "mm":
                label += date.strftime("%m")
            elif item == "mmm":
                label += date.strftime("%b")
            else:
                label += date.strftime("%B")
        elif "d".upper() in item.upper():
            if item == "d":
                label += str(date.day)
            else:
                label += date.strftime("%d")
        elif "a".upper() in item.upper():
            if item in ["a", "aa"]:
                label += date.strftime("%a")[0]
            elif item == "aaa":
                label += date.strftime("%a")
            else:
                label += date.strftime("%A")
        elif "n".upper() in item.upper():
            if item in ["n", "nn"]:
                label += str(date.timetuple()[7])
            else:
                label += date.strftime("%j")
        elif "w".upper() in item.upper():
            if week_start == 0:
                label += date.strftime("%W")
            else:
                label += date.strftime("%U")
        else:
            raise ValueError(item)

        label += " "

    return label.strip().replace(" ", str(separator))

