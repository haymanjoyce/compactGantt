# todo create tabs
# todo create display
# todo ability to save and load files
# todo ability to import and export as spreadsheet
# todo ability to print image
# todo ability to render SVG image

import wx
from wx import svg
from tabs import ListCtrl
import chart


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        chart_svg = chart.build_chart()
        chart_bytes = chart_svg.encode(encoding='utf-8')

        self.img = wx.svg.SVGimage.CreateFromBytes(chart_bytes)  # cannot resolve PyCharm complaint
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        # dcdim = min(self.Size.width, self.Size.height)
        # imgdim = min(self.img.width, self.img.height)
        # scale = dcdim / imgdim
        # width = int(self.img.width * scale)
        # height = int(self.img.height * scale)

        ctx = wx.GraphicsContext.Create(dc)
        self.img.RenderToGC(ctx, scale=1)


class ListCtrlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        tab = ListCtrl(self, wx.NewIdRef(), style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)


class NoteBookPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        notebook = wx.Notebook(self)
        tab_1 = ListCtrlPanel(notebook)
        tab_2 = ListCtrlPanel(notebook)
        tab_3 = ListCtrlPanel(notebook)
        notebook.AddPage(tab_1, "Tab 1")
        notebook.AddPage(tab_2, "Tab 2")
        notebook.AddPage(tab_3, "Tab 3")

        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # # Create a panel and notebook (tabs holder)
        # p = wx.Panel(self)
        # nb = wx.Notebook(p)
        #
        # # Create the tab windows
        # tab1 = TabOne(nb)
        # tab2 = TabTwo(nb)
        # tab3 = TabThree(nb)
        # tab4 = TabFour(nb)
        #
        # # Add the windows to tabs and name them.
        # nb.AddPage(tab1, "Tab 1")
        # nb.AddPage(tab2, "Tab 2")
        # nb.AddPage(tab3, "Tab 3")
        # nb.AddPage(tab4, "Tab 4")
        #
        # # Set noteboook in a sizer to create the layout
        # sizer = wx.BoxSizer()
        # sizer.Add(nb, 1, wx.EXPAND)
        # p.SetSizer(sizer)

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(tab, 1, wx.EXPAND)
        # self.SetSizer(sizer)
        # self.SetAutoLayout(True)


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')

        splitter = wx.SplitterWindow(self)
        left = NoteBookPanel(splitter)
        right = ImagePanel(splitter)
        splitter.SplitVertically(left, right)
        splitter.SetMinimumPaneSize(100)
        splitter.SetSashPosition(200, redraw=True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(sizer)


class App(wx.App):
    def __init__(self):
        super().__init__(redirect=False)

    def run(self):
        frame = Frame()
        frame.Show()
        self.MainLoop()

