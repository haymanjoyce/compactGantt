# todo decide how you're going to store data (CSV or XML)
# todo ability to validate inputs and highlight if error or run health check
# todo ability to export data
# todo menu
# todo automatically set column wx.LIST_FORMAT_RIGHT according to data type

import wx
import wx.lib.mixins.listctrl as listmix
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


class Table(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID=wx.NewIdRef(), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)

        self.SetWindowStyle(wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SORT_ASCENDING | wx.BORDER_NONE)

        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.on_being_label_edit)

    def insert_columns(self, columns):
        for column in columns:
            index = columns.index(column)
            self.InsertColumn(index, column, wx.LIST_FORMAT_LEFT)

    def insert_rows(self, quantity):
        for row in range(quantity):
            self.InsertItem(row, 0)  # second argument is data (using 0 as default)

    def import_by_column(self, data):
        for column in range(self.GetColumnCount()):
            values = data.get(self.GetColumn(column).GetText())
            row = 0
            for value in values:
                self.SetItem(row, column, value)
                row += 1

    def import_by_row(self, data):
        for row, values in data.items():
            self.InsertItem(row, values[0])
            column = 1
            for value in values[1:]:
                self.SetItem(row, column, value)
                column += 1

    def export_data(self):
        data = {}
        for row in range(self.GetItemCount()):
            data[row] = [self.GetItem(row, col).GetText() for col in range(self.GetColumnCount())]
        return data

    def autosize_columns(self):
        for col in range(self.GetColumnCount()):
            self.SetColumnWidth(col, wx.LIST_AUTOSIZE)  # second argument is pixels

    def set_cell_data(self, row, col, data):
        wx.ListCtrl.SetItem(self, row, col, data)

    def get_cell_data(self, row, col):
        data = self.GetItem(row, col).GetText()
        return data

    def on_being_label_edit(self, event):
        if event.Column == 1:
            event.Veto()  # makes cell read only
        else:
            event.Skip()  # event available for another event handler


class Tab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.table = Table(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.table, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)

        tab_1 = Tab(self)
        tab_2 = Tab(self)

        self.AddPage(tab_1, "Tab 1")
        self.AddPage(tab_2, "Tab 2")

        tab_1.table.insert_columns(scale_fields)
        tab_1.table.insert_rows(2)
        tab_1.table.import_by_column(scale_column_data)

        tab_2.table.insert_columns(scale_fields)
        tab_2.table.import_by_row(scale_row_data)

        # self.insert_columns()
        # self.insert_rows(len(scale_data))
        # self.import_data(scale_data.items())


class Window(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')
        self.tabs = Tabs(self)

