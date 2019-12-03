#!/usr/bin/env python3

# ENV02

import shapes

style_a = shapes.Style(fill="red")
print(style_a)

rectangle_a = shapes.Rectangle(height=10, width=20, style=style_a)
print(rectangle_a)

frame_a = shapes.Frame()
print(frame_a)


