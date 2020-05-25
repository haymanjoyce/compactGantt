# todo ability to create custom interval (e.g. 20 days representing 1 month)
# todo rewrite as a class

from datetime import date


def clean_interval_type(func):
    def inner(*args, **kwargs):
        args = list(args)
        interval_type = args[3].lower()
        if interval_type in ['days', 'day', 'd', '']:
            args[3] = 'DAYS'
        elif interval_type in ['weeks', 'week', 'wk', 'w']:
            args[3] = 'WEEKS'
        elif interval_type in ['months', 'mon', 'month', 'm']:
            args[3] = 'MONTHS'
        elif interval_type in ['quarters', 'quarts', 'qts', 'q']:
            args[3] = 'QUARTERS'
        elif interval_type in ['halves', 'half', 'halfs', 'halve', 'h']:
            args[3] = 'HALVES'
        elif interval_type in ['years', 'year', 'yrs', 'yr', 'y']:
            args[3] = 'YEARS'
        else:
            raise ValueError(args[3])
        args = tuple(args)
        return func(*args, **kwargs)
    return inner


@clean_interval_type
def select_intervals(x, start, finish, interval_type='DAYS', resolution=1.0, week_start=0):
    """Returns iterable containing data for building Scale or Grid intervals"""

    # Returned iterable is a tuple of tuples
    # Each tuple: x (pixels), width (pixels), ordinal date (00:00hrs of date), count (starting at 1), whole (boolean)

    if interval_type == 'DAYS':
        return days(x, start, finish, resolution)

    elif interval_type == 'WEEKS':
        return weeks(x, start, finish, resolution, week_start)

    elif interval_type == 'MONTHS':
        start_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, wholes)

    elif interval_type == 'QUARTERS':
        start_months = [1, 4, 7, 10]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, wholes)

    elif interval_type == 'HALVES':
        start_months = [1, 7]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, wholes)

    elif interval_type == 'YEARS':
        start_months = [1]
        wholes = whole_starts(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, wholes)

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

