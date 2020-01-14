from dataclasses import dataclass, field
from calendar import *

# smallest unit of time is 1 second
# smallest resolution is 1 pixel
# give each interval a width
# width must be proportional to time (seconds) elapsed
# width will be ratio of pixels to seconds


@dataclass
class Window:

    start_date: int
    finish_date: int
    time_interval: str  # hour | day | week | month | quarter | year
    calendar_type: str  # normal | ordinal
    time_order: str  # normal | reverse

    def get(self):
        window = Calendar(firstweekday=0)
        return window.iterweekdays()

