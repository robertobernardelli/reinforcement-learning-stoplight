from car import *
from stoplight import *

stl = []
cal = []

sl1 = Stop_list()
cl1 = Car_list()
sl1.append(Stoplight((420, 601), first = True))
sl1.append(Stoplight((420, 600)))
sl1.append(Stoplight((420, 360), red = True, fake = False))
sl1.append(Stoplight((420, 0), last = True))
stl.append(sl1)
cal.append(cl1)

sl2 = Stop_list()
cl2 = Car_list()
sl2.append(Stoplight((370, -1), first = True))
sl2.append(Stoplight((370, 0)))
sl2.append(Stoplight((370, 220), red = True, fake = False))
sl2.append(Stoplight((370, 600), last = True))


stl.append(sl2)
cal.append(cl2)

sl3 = Stop_list()
cl3 = Car_list()
sl3.append(Stoplight((-1, 320), first = True))
sl3.append(Stoplight((0, 320)))
sl3.append(Stoplight((340, 320), fake = False))
sl3.append(Stoplight((800, 320), last = True))


stl.append(sl3)
cal.append(cl3)

sl4 = Stop_list()
cl4 = Car_list()
sl4.append(Stoplight((801, 280), first = True))
sl4.append(Stoplight((800, 280)))
sl4.append(Stoplight((440, 280), fake = False))
sl4.append(Stoplight((0, 280), last = True))


stl.append(sl4)
cal.append(cl4)