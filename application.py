# todo create tabs
# todo create display
# todo ability to save and load files
# todo ability to import and export as spreadsheet
# todo ability to print image
# todo ability to render SVG image

import wx
from tabs import ListCtrl


class ListCtrlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        tab = ListCtrl(self, wx.NewIdRef(), style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tab, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


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

