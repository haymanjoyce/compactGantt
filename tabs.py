# todo review data structure and location
# todo enter data into table as parameter
# todo decide how you're going to store and import/export data (CSV, XML, file, db)
# todo ability to validate inputs and highlight if error or run health check
# todo menu

import wx
import wx.grid as grid
import wx.lib.gridmovers as gridmovers
from pprint import pprint as pp

scale_fields = ('Start', 'Finish', 'Date Format')

scale_column_data = {
    'Start': ('1 Jan 20', '5 Jan 20'),
    'Finish': ('20 Jan 20', '25 Jan 20'),
    'Date Format': ('dd mm yy', 'dd mm yy'),
}

scale_row_data = {
    0: ('1 Jan 20', '20 Jan 20', 'dd mm yy'),
    1: ('5 Jan 20', '25 Jan 20', 'dd mm yy'),
}

identifiers = ['id', 'ds', 'sv', 'pr', 'pl', 'op', 'fx', 'ts']

row_labels = ['Row1', 'Row2', 'Row3']

col_labels = {'id': 'ID', 'ds': 'Description', 'sv': 'Severity',
              'pr': 'Priority', 'pl': 'Platform', 'op': 'Opened?',
              'fx': 'Fixed?', 'ts': 'Tested?'}

data = [{'id': 1010,
         'ds': "The foo doesn't bar",
         'sv': "major",
         'pr': 1,
         'pl': 'MSW',
         'op': 1,
         'fx': 1,
         'ts': 1
         },
        {'id': 1011,
         'ds': "I've got a wicket in my wocket",
         'sv': "wish list",
         'pr': 2,
         'pl': 'other',
         'op': 0,
         'fx': 0,
         'ts': 0
         },
        {'id': 1012,
         'ds': "Rectangle() returns a triangle",
         'sv': "critical",
         'pr': 5,
         'pl': 'all',
         'op': 0,
         'fx': 0,
         'ts': 0
         }
        ]


class Table(grid.GridTableBase):
    """Holds the data.  Usually wx.grid.GridStringTable is used but gridmovers requires customisation of base class."""
    def __init__(self):
        grid.GridTableBase.__init__(self)

    # our custom class must override these methods (i.e. the base class interface)

    def GetNumberRows(self):
        return len(data)

    def GetNumberCols(self):
        return len(identifiers)

    def IsEmptyCell(self, row, col):
        key = identifiers[col]
        return not data[row][key]

    def GetValue(self, row, col):
        key = identifiers[col]
        return str(data[row][key])

    def SetValue(self, row, col, value):
        key = identifiers[col]
        data[row][key] = value

    # we want custom column and row labels and so we override these methods

    def GetColLabelValue(self, col):
        identifier = identifiers[col]
        return col_labels[identifier]

    def GetRowLabelValue(self, row):
        return row_labels[row]

    # event handler changes the table (i.e. data) and then the grid

    def move_column(self, mover_col, index_col):

        def change_table():
            old = identifiers[mover_col]
            del identifiers[mover_col]
            if index_col > mover_col:
                identifiers.insert(index_col - 1, old)
            else:
                identifiers.insert(index_col, old)

        def change_grid():
            view.BeginBatch()
            msg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_COLS_DELETED, mover_col, 1)
            view.ProcessTableMessage(msg)
            msg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_COLS_INSERTED, index_col, 1)
            view.ProcessTableMessage(msg)
            view.EndBatch()

        view = self.GetView()

        if view:
            change_table()
            change_grid()

    def move_row(self, mover_row, index_row):

        def change_table():
            old_label = row_labels[mover_row]
            old_data = data[mover_row]
            del row_labels[mover_row]
            del data[mover_row]
            if index_row > mover_row:
                row_labels.insert(index_row - 1, old_label)
                data.insert(index_row - 1, old_data)
            else:
                row_labels.insert(index_row, old_label)
                data.insert(index_row, old_data)

        def change_grid():
            view.BeginBatch()
            msg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_ROWS_DELETED, mover_row, 1)
            view.ProcessTableMessage(msg)
            msg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_ROWS_INSERTED, index_row, 1)
            view.ProcessTableMessage(msg)
            view.EndBatch()

        view = self.GetView()

        if view:
            change_table()
            change_grid()


class Grid(grid.Grid):
    """Grids are for viewing the data held by GridTableBase.  One dataset to many views."""
    def __init__(self, parent, table):
        grid.Grid.__init__(self, parent, -1)

        # we set grid to own and, therefore, control table
        # SetTable assigns table to pre-defined attribute "Table", I suspect
        # self.table also works but creates new attribute "table"
        # interestingly, self.table, with ownership set to False, works
        self.SetTable(table, takeOwnership=True)

        gridmovers.GridColMover(self)
        self.Bind(event=gridmovers.EVT_GRID_COL_MOVE, handler=self.on_col_move, source=self)

        gridmovers.GridRowMover(self)
        self.Bind(event=gridmovers.EVT_GRID_ROW_MOVE, handler=self.on_row_move, source=self)

    def on_col_move(self, event):
        mover_col = event.GetMoveColumn()  # column being moved
        index_col = event.GetBeforeColumn()  # before which column to insert
        self.GetTable().move_column(mover_col, index_col)  # Grid asks Table to do some work

    def on_row_move(self, event):
        mover_row = event.GetMoveRow()  # row being moved
        index_row = event.GetBeforeRow()  # before which row to insert
        self.GetTable().move_row(mover_row, index_row)  # Grid asks Table to do some work


class Tabs(wx.Notebook):
    """We need tabs to display all the different tables.  (I've renamed the class.)"""
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)

        table_a = Table()
        table_b = Table()

        tab_1 = Grid(parent=self, table=table_a)
        tab_2 = Grid(parent=self, table=table_b)

        self.AddPage(tab_1, "Tab 1")
        self.AddPage(tab_2, "Tab 2")


class Window(wx.Frame):
    """The main window.  wx.Window is used for something else so they called it wx.Frame."""
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')

        menubar = wx.MenuBar()

        file = wx.Menu()

        open_file = wx.MenuItem(file, wx.ID_NEW, text="Open", kind=wx.ITEM_NORMAL)

        file.Append(open_file)

        menubar.Append(file, "File")

        self.SetMenuBar(menubar)

        self.tabs = Tabs(self)
