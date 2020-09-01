#!/usr/bin/env python3

import wx
import tabs
import chart


class App(wx.App):
    def __init__(self):
        super().__init__(redirect=False)
        self.frame_1 = tabs.Window()
        # self. frame_2 = chart.ChartFrame()

    def run(self):
        self.frame_1.Show()
        # self.frame_2.Show()
        self.MainLoop()


if __name__ == "__main__":
    app = App()
    app.run()


# REQUIREMENTS
# attrs
# wxPython
# pandas

# todo ability to save and load files
# todo ability to import and export as spreadsheet
# todo ability to print image
# todo ability to render SVG image
# todo render svg using wx
# todo gui
# todo banners module
# todo columns module
# todo titles module
# todo plot module
# todo textbox module
# todo image module
# todo table module
