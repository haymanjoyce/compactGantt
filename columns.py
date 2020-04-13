"""Module defines layout"""

# todo time window height determined by scale heights and row heights

from dataclasses import dataclass


@dataclass
class ColumnHeader:

    header_fill_color: str
    header_border_width: float
    header_border_color: str


@dataclass
class ColumnTitle:
    pass


@dataclass
class Columns:

    quantity: int
    default_width: float
    header_row_height: float

    column_fill_color: str
    column_border_color: str
    column_border_width: str

    header_fill_color: str
    header_border_width: float
    header_border_color: str

    def clean_columns(self):
        pass

    def build_columns(self):
        pass

    def get_columns(self):
        pass


@dataclass
class Column:

    column_number: int  # the column name (1 is leftmost)
    column_width: int  # can override default width
    column_placement: str  # if a column is placed on the right, every column after it is placed on the right
    column_title: str

    column_fill_color: str
    column_border_color: str
    column_border_width: str

    column_header_fill_color: str
    column_header_border_width: float
    column_header_border_color: str

    def clean_column(self):
        pass

    def build_column(self):
        pass

    def get_column(self):
        pass

