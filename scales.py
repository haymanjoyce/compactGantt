from shapes import Box
import pprint

a1 = Box(x=0, y=0, width=10, height=50, border=1)

scale = []

def scale_a():

    for i in range(10):

        a1.x = (i * 10)
        pprint.pprint(a1.x)
        scale.append(a1)

    return scale

