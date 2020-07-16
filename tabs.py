# todo create tabs for different features
# todo ability to validate inputs and highlight if error

import wx
import wx.lib.mixins.listctrl as listmix
from abc import abstractmethod

scale_data = {
    1: ("Hey!", "You can edit", "me!"),
    2: ("Try changing the contents", "by", "clicking"),
    3: ("in", "a", "cell"),
    4: ("See how the length columns", "change", "?"),
    5: ("You can use", "TAB,", "cursor down,"),
    6: ("and cursor up", "to", "navigate"),
    }

grid_data = {
    1: ("Ho!!", "You can edit", "me!"),
    2: ("Try changing the contents", "by", "clicking"),
    3: ("in", "a", "cell"),
    4: ("See how the length columns", "change", "?"),
    5: ("You can use", "TAB,", "cursor down,"),
    6: ("and cursor up", "to", "navigate"),
    }


class Table(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID=wx.NewIdRef(), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)

        self.SetWindowStyle(wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SORT_ASCENDING | wx.BORDER_NONE)
        self.currentItem = 0  # sets current row
        self.cols = self.GetColumnCount()
        self.rows = self.GetItemCount()

        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)

    @abstractmethod
    def insert_columns(self):
        pass

    def autosize_columns(self):
        for col in range(self.cols):
            self.SetColumnWidth(col, wx.LIST_AUTOSIZE)  # second argument is pixels

    def insert_rows(self, quantity):
        for row in range(quantity):
            self.InsertItem(row, 0)  # second argument is data (using 0 as default)

    def import_data(self, data):
        row = 0
        for key, value in data:
            self.SetItem(row, 0, value[0])
            self.SetItem(row, 1, value[1])
            self.SetItem(row, 2, value[2])
            self.SetItemData(row, key)
            row += 1

    def export_data(self):
        data = {}
        for row in range(self.rows):
            data[row] = [self.GetItem(row, col).GetText() for col in range(self.cols)]
        return data

    def set_cell_data(self, row, col, data):
        wx.ListCtrl.SetItem(self, row, col, data)

    def get_cell_data(self, row, col):
        data = self.GetItem(row, col).GetText()
        return data

    def OnBeginLabelEdit(self, event):
        print(event)
        # if event.m_col == 1:
        #     event.Veto()
        # else:
        #     event.Skip()


class Scales(Table):
    def __init__(self, parent):
        super().__init__(parent)

        self.insert_columns()
        self.insert_rows(len(scale_data))
        self.import_data(scale_data.items())
        self.autosize_columns()
        self.export_data()
        self.set_cell_data(0, 4, "5")
        self.get_cell_data(0, 1)

    def insert_columns(self):
        self.InsertColumn(0, "Column 1")
        self.InsertColumn(1, "Column 2")
        self.InsertColumn(2, "Column 3")
        self.InsertColumn(3, "Len 1", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(4, "Len 2", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(5, "Len 3", wx.LIST_FORMAT_RIGHT)


class Grid(Table):
    def __init__(self, parent):
        super().__init__(parent)

        self.insert_columns()
        self.insert_rows(len(grid_data))
        self.import_data(grid_data.items())
        self.autosize_columns()
        self.export_data()
        self.set_cell_data(0, 4, "5")
        self.get_cell_data(0, 1)

    def insert_columns(self):
        self.InsertColumn(0, "Column 1")
        self.InsertColumn(1, "Column 2")
        self.InsertColumn(2, "Column 3")
        self.InsertColumn(3, "Len 1", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(4, "Len 2", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(5, "Len 3", wx.LIST_FORMAT_RIGHT)


class Tab(wx.Panel):
    def __init__(self, parent, table):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.table = table(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.table, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)

        tab_1 = Tab(self, Scales)
        tab_2 = Tab(self, Grid)

        self.AddPage(tab_1, "Tab 1")
        self.AddPage(tab_2, "Tab 2")
        

class Window(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')
        self.tabs = Tabs(self)

