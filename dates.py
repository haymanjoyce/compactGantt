from datetime import date


def convert_ordinal(ordinal_date, date_format, week_start=0, separator=' '):
    """Converts ordinal date into custom date format"""

    # todo ability to prefix date format (e.g. Week 2, Q2, Half 2) (replaces Q, H, and Y)
    # todo improve speed (e.g. by making it class)

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

    dt = date.fromordinal(ordinal_date)

    day = dt.day
    month = dt.month

    items = str(date_format).strip().split()

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
            if week_start == 0:
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


def select_scale(x, start, finish, interval_type='DAYS', pixels_per_day=1.0, week_start=0):
    """Selects appropriate iterable based on interval type"""

    # Iterable is a tuple of tuples
    # Each tuple: x (pixels), width (pixels), ordinal date (00:00hrs of date), count, whole (boolean)

    # todo ability to create custom interval (e.g. 20 days representing 1 month)

    if interval_type == 'DAYS':
        return days(x, start, finish, pixels_per_day)

    elif interval_type == 'WEEKS':
        return weeks(x, start, finish, pixels_per_day, week_start)

    elif interval_type == 'MONTHS':
        start_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, pixels_per_day, wholes)

    elif interval_type == 'QUARTERS':
        start_months = [1, 4, 7, 10]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, pixels_per_day, wholes)

    elif interval_type == 'HALVES':
        start_months = [1, 7]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, pixels_per_day, wholes)

    elif interval_type == 'YEARS':
        start_months = [1]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, pixels_per_day, wholes)

    else:
        raise ValueError(interval_type)


def days(x, start, finish, resolution):
    """Returns iterable showing all days in a given range"""

    entries = tuple()
    total_days = finish - start
    width = 1 * resolution

    for day in range(total_days):

        entry = x, width, start + day, day + 1, True
        entries += (entry, )
        x += width

    return entries


def weeks(x, start, finish, resolution, week_start):
    """Returns iterable showing all weeks in a given range"""

    entries = tuple()
    intervals = [day for day in range(start, finish + 1) if date.fromordinal(day).weekday() == week_start or day == start or day == finish]
    interval = 0
    width = 0
    count = 0

    while intervals[interval] != finish:

        current_start = intervals[interval]
        next_start = intervals[interval + 1]

        duration = next_start - current_start

        if current_start == start and duration < 7:
            whole = False
        elif next_start == finish and duration < 7:
            whole = False
            count += 1
        else:
            whole = True
            count += 1

        x += width
        width = duration * resolution

        entry = x, width, current_start, count, whole
        entries += (entry, )

        interval += 1

    return entries


def whole_starts(start, finish, start_months):
    """Returns start dates for all Gregorian periods in given range, including last day in range"""

    return [day for day in range(start, finish + 1) if date.fromordinal(day).month in start_months and date.fromordinal(day).day == 1]


def gregorian_periods(x, start, finish, resolution, whole_intervals):
    """Returns iterable showing all Gregorian periods (greater or equal to one month) in a given range"""

    entries = tuple()

    starts = whole_intervals.copy()

    if start not in starts:
        starts = [start] + starts

    if finish not in starts:
        starts = starts + [finish]

    interval = 0

    count = 0

    while starts[interval] != finish:

        current_start = starts[interval]

        next_start = starts[interval + 1]

        width = (next_start - current_start) * resolution

        if current_start == start and start not in whole_intervals:
            count += 0
            whole = False
        elif next_start == finish and finish not in whole_intervals:
            count += 1
            whole = False
        else:
            count += 1
            whole = True

        entry = x, width, current_start, count, whole
        entries += (entry, )

        x += width

        interval += 1

    return entries

