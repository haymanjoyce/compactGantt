# todo how export data

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

    def SetStringItem(self, index, col, data):
        if col in range(3):
            wx.ListCtrl.SetItem(self, index, col, data)
            wx.ListCtrl.SetItem(self, index, 3+col, str(len(data)))
        else:
            try:
                datalen = int(data)
            except:
                return

            wx.ListCtrl.SetItem(self, index, col, data)

            data = self.GetItem(index, col-3).GetText()
            wx.ListCtrl.SetItem(self, index, col-3, data[0:datalen])


class ListCtrlPanel(wx.Panel):
    def __init__(self, parent, log=None):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.log = log
        tID = wx.NewIdRef()

        sizer = wx.BoxSizer(wx.VERTICAL)

        if wx.Platform == "__WXMAC__" and \
               hasattr(wx.GetApp().GetTopWindow(), "LoadDemo"):
            self.useNative = wx.CheckBox(self, -1, "Use native listctrl")
            self.useNative.SetValue(
                not wx.SystemOptions.GetOptionInt("mac.listctrl.always_use_generic") )
            self.Bind(wx.EVT_CHECKBOX, self.OnUseNative, self.useNative)
            sizer.Add(self.useNative, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        self.list = ListCtrl(self, tID,
                             style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 #| wx.LC_SORT_ASCENDING            # Content of list as instructions is
                                 | wx.LC_HRULES | wx.LC_VRULES  # nonsense with auto-sort enabled
                             )

        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnUseNative(self, event):
        wx.SystemOptions.SetOption("mac.listctrl.always_use_generic", not event.IsChecked())
        wx.GetApp().GetTopWindow().LoadDemo("ListCtrl_edit")


class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')
        panel = ListCtrlPanel(self)
        self.Show()


class App(wx.App):

    def __init__(self):
        super().__init__(redirect=False)

    def run(self):
        frame = Frame()
        self.MainLoop()

