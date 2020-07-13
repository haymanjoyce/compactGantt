# todo create tabs for different features
# todo ability to validate inputs and highlight if error

import wx
import wx.lib.mixins.listctrl as listmix


listctrldata = {
    1: ("Hey!", "You can edit", "me!"),
    2: ("Try changing the contents", "by", "clicking"),
    3: ("in", "a", "cell"),
    4: ("See how the length columns", "change", "?"),
    5: ("You can use", "TAB,", "cursor down,"),
    6: ("and cursor up", "to", "navigate"),
    }


class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)

        self.insert_columns()
        self.insert_rows(len(listctrldata))
        self.import_data(listctrldata.items())
        self.resize_columns()
        self.currentItem = 0
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

    def resize_columns(self):
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, 100)

    def insert_rows(self, quantity):
        for row in range(quantity):
            self.InsertItem(row, 0)

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
        cols = self.GetColumnCount()
        rows = self.GetItemCount()
        for row in range(rows):
            data[row] = [self.GetItem(row, col).GetText() for col in range(cols)]
        return data

    def set_cell_data(self, row, col, data):
        wx.ListCtrl.SetItem(self, row, col, data)

    def get_cell_data(self, row, col):
        data = self.GetItem(row, col).GetText()
        return data


class Tab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.tab_1 = ListCtrl(self, wx.NewIdRef(),
                              style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)
        self.tab_2 = ListCtrl(self, wx.NewIdRef(),
                              style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)
        self.tab_3 = ListCtrl(self, wx.NewIdRef(),
                              style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)


class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)

        tab_1 = Tab(self)
        tab_2 = Tab(self)
        tab_3 = Tab(self)
        self.AddPage(tab_1, "Tab 1")
        self.AddPage(tab_2, "Tab 2")
        self.AddPage(tab_3, "Tab 3")


class TabsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')

        panel = Tabs(self)

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(panel, wx.ID_ANY, wx.EXPAND)
        # self.SetSizer(sizer)
        # self.SetAutoLayout(True)

