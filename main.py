#!/usr/bin/env python3

# ENV02


import shapes

style_a = shapes.Style(fill="green")
print(style_a)

rectangle_a = shapes.Rectangle(height=10, width=20, style=str(style_a))
print(rectangle_a)

frame_a = shapes.Box(x=100, y=100, width=300, height=100, stroke_width=5)
frame_b = shapes.Box(x=100, y=200, width=300, height=100, stroke_width=10)
frame_c = shapes.Box(x=100, y=300, width=300, height=100, stroke_width=0, padding=0, style=str(style_a))
print(frame_a, frame_b, frame_c)


