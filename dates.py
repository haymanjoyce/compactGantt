"""Module for handling dates"""

# todo conditionals in if x in [a, b, c] format to interpret date person is after
# todo will need label entries to be tuples with order as one of the values
# todo raise value error if format does not apply to interval type

import datetime as dt


def change_format(ordinal_date, date_format='mm', week_start=0, separator=' ', label_type='d'):

    date = dt.date.fromordinal(ordinal_date)
    label = str()

    if date_format in ['mm']:
        label += str(date.day)

    return label


def conversions():
    """List of all the ways to convert an ordinal"""

    delta = dt.timedelta(days=10)
    today = dt.date.today() + delta
    today = today.toordinal()
    today = dt.date.fromordinal(today)

    print("years:")
    # print(today.year)
    print(today.strftime("%y"), "y or yy")
    print(today.strftime("%Y"), "any other kind of y or Y")

    print()
    print("months:")
    print(today.month, "m")
    print(today.strftime("%m"), "mm")
    print(today.strftime("%b"), "mmm")
    print(today.strftime("%B"), "M expected but any other kind of m or M accepted")

    print()
    print("dates:")
    print(today.day, "d")
    print(today.strftime("%d"), "dd expected but any other kind of d or D accepted")

    print()
    print("day names:")
    print(today.strftime("%a")[0], "a or aa")
    print(today.strftime("%a"), "aaa")
    print(today.strftime("%A"), "A expected but any other kind of a or A accepted")

    print()
    print("day of the week as number (not an option):")
    print(today.weekday(), "")

    print()
    print("day of the year as number (where 1 Jan is day 1):")
    print(today.timetuple()[7], "n or nn")
    print(today.strftime("%j"), "nnn expected but any other kind of n or N accepted")

    print()
    print("week number (where week_start determines which, automatically):")
    print(today.strftime("%U"), "w expected but any kind of w or W accepted (w/c Sunday)")
    print(today.strftime("%W"), "w expected but any kind of w or W accepted (w/c Monday)")


conversions()



