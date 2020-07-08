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


class ListCtrlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        tab = ListCtrl(self, wx.NewIdRef(), style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING | wx.LC_HRULES | wx.LC_VRULES)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tab, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.chart_svg = chart.build_chart()
        self.chart_bytes = self.chart_svg.encode(encoding='utf-8')

        self.img = wx.svg.SVGimage.CreateFromBytes(self.chart_bytes)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        dcdim = min(self.Size.width, self.Size.height)
        imgdim = min(self.img.width, self.img.height)
        scale = dcdim / imgdim
        width = int(self.img.width * scale)
        height = int(self.img.height * scale)

        ctx = wx.GraphicsContext.Create(dc)
        self.img.RenderToGC(ctx, scale)


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')
        # panel = ListCtrlPanel(self)
        image = ImagePanel(self)
        self.Show()


class App(wx.App):
    def __init__(self):
        super().__init__(redirect=False)

    def run(self):
        frame = Frame()
        self.MainLoop()

