from attr import attrs, attrib


@attrs
class Interval:
    pass


# SOME OF THIS STUFF BELONGS HERE, SOME IN SCALES MODULE

# scale_x: float = 0
# scale_y: float = 0

# week_start_text: str = str(0)

# week_start_num: int = 0

# interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

# interval_data: tuple = tuple()

# def get_interval_data(self):
#     return select_scale(self.scale_x, self.window_start, self.window_finish, self.interval_type, self._pixels_per_day, self.week_start_num)

# clean interval type
# if self.interval_type.lower() in [item.lower() for item in
#                                   ['days', 'day', 'd', '']]:  # blank indicates default
#     self.interval_type = 'DAYS'
# elif self.interval_type.lower() in [item.lower() for item in ['weeks', 'week', 'wk', 'w']]:
#     self.interval_type = 'WEEKS'
# elif self.interval_type.lower() in [item.lower() for item in ['months', 'mon', 'month', 'm']]:
#     self.interval_type = 'MONTHS'
# elif self.interval_type.lower() in [item.lower() for item in ['quarters', 'quarts', 'qts', 'q']]:
#     self.interval_type = 'QUARTERS'
# elif self.interval_type.lower() in [item.lower() for item in ['halves', 'half', 'halfs', 'halve', 'h']]:
#     self.interval_type = 'HALVES'
# elif self.interval_type.lower() in [item.lower() for item in ['years', 'year', 'yrs', 'yr', 'y']]:
#     self.interval_type = 'YEARS'
# else:
#     raise ValueError(self.interval_type)

# clean first day of week string, if given, and converts to integer
# if self.week_start_text in ['6', '7', 'S', 'Sun', 'Sunday', 'SUN', 'SUNDAY']:
#     self.week_start_num = 6
# else:
#     self.week_start_num = 0

