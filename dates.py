"""Module for handling dates"""

# todo ability to prefix date format (e.g. Week 2, Q2, Half 2) (replaces Q, H, and Y)
# todo improve speed (e.g. by making it class)

import datetime as dt


def convert_ordinal(ordinal_date, date_format, week_start=0, separator=' '):
    """Converts ordinal date into custom date format"""

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

    if week_start not in [0, 6]:  # Python only handles Mondays or Sundays
        week_start = 0

    date = dt.date.fromordinal(ordinal_date)

    day = date.day
    month = date.month

    items = str(date_format).strip().split()

    label = str()

    for item in items:

        if "y".upper() in item.upper():
            if item == "y":
                label += date.strftime("%y")
            elif item == "Y":
                label += "Y" + date.strftime("%y")
            else:
                label += date.strftime("%Y")
        elif "m".upper() in item.upper():
            if item == "m":
                label += str(month)
            elif item == "mm":
                label += date.strftime("%m")
            elif item == "mmm":
                label += date.strftime("%b")
            else:
                label += date.strftime("%B")
        elif "d".upper() in item.upper():
            if item == "d":
                label += str(day)
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

    return label.strip().replace(" ", str(separator))


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

