from abc import abstractmethod


class Base:

    def __init__(self, position=0):
        self.position = position

    @abstractmethod
    def __call__(self, func):
        def new_func(*args, **kwargs):
            args = list(args)
            try:
                argument = str(args[self.position]).lower()
                # clean argument here
            except IndexError:
                pass  # log no argument passed
            args = tuple(args)
            return func(*args, **kwargs)
        return new_func


class Separator(Base):

    def __call__(self, func):
        def new_func(*args, **kwargs):
            args = list(args)
            try:
                argument = str(args[self.position]).lower()
                if len(argument) > 1 or argument in ['%', '#', '?', '*', '\"'] or argument.isdigit():
                    args[self.position] = '-'  # default
            except IndexError:
                pass
            args = tuple(args)
            return func(*args, **kwargs)
        return new_func


class WeekStart(Base):

    def __call__(self, func):
        def new_func(*args, **kwargs):
            args = list(args)
            try:
                argument = str(args[self.position]).lower()
                if argument in ['6', '7', 'S', 'Sun', 'Sunday', 'SUN', 'SUNDAY']:
                    args[self.position] = 6
                else:
                    args[self.position] = 0
            except IndexError:
                pass  # log first day of week not passed
            args = tuple(args)
            return func(*args, **kwargs)
        return new_func


class IntervalType(Base):

    def __call__(self, func):
        def new_func(*args, **kwargs):
            args = list(args)
            try:
                argument = str(args[self.position]).lower()
                if argument in ['days', 'day', 'd', '']:
                    args[self.position] = 'DAYS'
                elif argument in ['weeks', 'week', 'wk', 'w']:
                    args[self.position] = 'WEEKS'
                elif argument in ['months', 'mon', 'month', 'm']:
                    args[self.position] = 'MONTHS'
                elif argument in ['quarters', 'quarts', 'qts', 'q']:
                    args[self.position] = 'QUARTERS'
                elif argument in ['halves', 'half', 'halfs', 'halve', 'h']:
                    args[self.position] = 'HALVES'
                elif argument in ['years', 'year', 'yrs', 'yr', 'y']:
                    args[self.position] = 'YEARS'
                else:
                    raise ValueError(args[self.position])
            except IndexError:
                pass  # log no argument passed
            args = tuple(args)
            return func(*args, **kwargs)
        return new_func

