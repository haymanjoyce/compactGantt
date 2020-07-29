# todo decide how you're going to store data (CSV or XML)
# todo ability to validate inputs and highlight if error or run health check
# todo ability to export data
# todo menu

import wx
import wx.grid as grid
import wx.lib.gridmovers as gridmovers

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
    def __init__(self):
        grid.GridTableBase.__init__(self)

    # required methods for the wxPyGridTableBase interface
    # must use wx format in order to override

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

    # some optional methods
    # must use wx format in order to override

    # called when the grid needs to display column labels
    def GetColLabelValue(self, col):
        key = identifiers[col]
        return col_labels[key]

    # called when the grid needs to display row labels
    def GetRowLabelValue(self, row):
        return row_labels[row]

    # the physical moving of the cols and rows is left to the implementer

    def move_column(self, frm, to):
        tab = self.GetView()

        if tab:
            # move the identifiers
            old = identifiers[frm]
            del identifiers[frm]

            if to > frm:
                identifiers.insert(to - 1, old)
            else:
                identifiers.insert(to, old)

            # Notify the grid
            tab.BeginBatch()
            msg = grid.GridTableMessage(
                self, grid.GRIDTABLE_NOTIFY_COLS_DELETED, frm, 1
            )

            tab.ProcessTableMessage(msg)

            msg = grid.GridTableMessage(
                self, grid.GRIDTABLE_NOTIFY_COLS_INSERTED, to, 1
            )

            tab.ProcessTableMessage(msg)
            tab.EndBatch()

    def move_row(self, frm, to):
        tab = self.GetView()
        print(type(tab))

        if tab:
            # move the rowLabels and data rows
            old_label = row_labels[frm]
            old_data = data[frm]
            del row_labels[frm]
            del data[frm]

            if to > frm:
                row_labels.insert(to - 1, old_label)
                data.insert(to - 1, old_data)
            else:
                row_labels.insert(to, old_label)
                data.insert(to, old_data)

            # notify the grid
            tab.BeginBatch()

            msg = grid.GridTableMessage(
                self, grid.GRIDTABLE_NOTIFY_ROWS_DELETED, frm, 1
            )

            tab.ProcessTableMessage(msg)

            msg = grid.GridTableMessage(
                self, grid.GRIDTABLE_NOTIFY_ROWS_INSERTED, to, 1
            )

            tab.ProcessTableMessage(msg)
            tab.EndBatch()


class Tab(grid.Grid):
    def __init__(self, parent, log=None):
        grid.Grid.__init__(self, parent, -1)

        table = Table()
        self.SetTable(table, takeOwnership=True)  # not clear why do not make table into an attribute

        # Enable Column moving
        gridmovers.GridColMover(self)
        self.Bind(gridmovers.EVT_GRID_COL_MOVE, self.OnColMove, self)

        # Enable Row moving
        gridmovers.GridRowMover(self)
        self.Bind(gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)

    # Event method called when a column move needs to take place
    def OnColMove(self, evt):
        frm = evt.GetMoveColumn()  # Column being moved
        to = evt.GetBeforeColumn()  # Before which column to insert
        self.GetTable().move_column(frm, to)

    # Event method called when a row move needs to take place
    def OnRowMove(self, evt):
        frm = evt.GetMoveRow()  # Row being moved
        to = evt.GetBeforeRow()  # Before which row to insert
        self.GetTable().move_row(frm, to)


class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)

        tab_1 = Tab(self)
        tab_2 = Tab(self)

        self.AddPage(tab_1, "Tab 1")
        self.AddPage(tab_2, "Tab 2")


class Window(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')
        self.tabs = Tabs(self)

