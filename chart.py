# todo rewrite

from datetime import date
from scales import Scale
from grid import Grid
from plot import Plot
from layout import Layout
from attr import attrs, attrib
import wx
from wx import svg


def build_chart():

    # LAYOUT
    layout = Layout()
    layout.configure(plot_width=1200)

    # TIME WINDOW
    today = date.toordinal(date.today())
    duration = 21
    end = today + duration

    # PLOT
    plot = Plot()
    plot.x = layout.plot.x
    plot.y = layout.plot.y
    plot.width = layout.plot.width
    plot.height = layout.plot.height
    plot.start = today
    plot.finish = end
    plot.clean_dates()
    plot.calculate_resolution()

    # SCALES
    scale = Scale()
    scale.x = layout.scales_top.x
    scale.y = layout.scales_top.y
    scale.width = layout.scales_top.width
    scale.height = layout.scales_top.height / 4
    scale.start = plot.start
    scale.finish = plot.finish
    scale.resolution = plot.resolution
    scale.interval_type = 'days'
    scale.week_start = 0
    scale.min_label_width = 20
    scale.box_fill = 'pink'
    scale.ends = 'yellow'
    scale.label_type = 'd'
    scale.date_format = 'a w'
    scale.separator = '-'
    scale.font_size = 10
    scale.text_x = 10
    scale.text_y = scale.height * 0.65

    # GRID
    grid = Grid()
    grid.interval_type = 'WEEKS'
    grid.week_start = 0
    grid.x = layout.plot.x
    grid.y = layout.plot.y
    grid.height = plot.height
    grid.start = plot.start
    grid.finish = plot.finish
    grid.resolution = plot.resolution
    grid.line_width = 0.5

    # VIEWPORT
    viewport = ViewPort()
    viewport.width = layout.chart.width
    viewport.height = layout.chart.height
    viewport.child_elements = [layout, scale, grid]
    viewport.order_child_elements()
    viewport.render_child_elements()

    return viewport.svg


@attrs
class ViewPort:
    """Objects represent the viewport, which is the SVG root element"""

    width = 800
    height = 600
    child_elements = attrib(default=list())
    svg_string = attrib(default=str())

    def order_child_elements(self):
        """Orders objects by their layer property"""
        pass

    def render_child_elements(self):
        """Builds SVG string; assumes all objects have an .svg property"""
        for child_element in self.child_elements:
            self.svg_string += child_element.svg

    def wrap_svg_string(self):
        """Wraps the SVG elements in the root SVG element"""
        return f'<svg width="{self.width}" height="{self.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self.svg_string}' \
               f'</svg>'

    @property
    def svg(self):
        """Returns SVG image which can be used by browser, GUI, and other clients"""
        return self.wrap_svg_string()


class ChartPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        chart_svg = build_chart()
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


class ChartFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='cG')

        panel = ChartPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

