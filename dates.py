"""Module for handling dates"""

# todo find every way to reformat an ordinal in Jupyter
# todo conditionals in if x in [a, b, c] format to interpret date person is after
# todo will need label entries to be tuples with order as one of the values

import datetime as dt


def temp(ordinal, date_format):

    date_format = 'day'
    date = dt.date.fromordinal(ordinal)
    label = str()

    # everything we can do with an ordinal
    if date_format in ['day', 'days', 'dd']:
        label += str(date.day)

    return label


