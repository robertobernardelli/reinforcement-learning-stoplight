from environment import *
from utils import *

intersection1 = Intersection()

intersection1.spawn_some_cars(10)

for timestep in range(1000):
    if timestep % 10 == 0:
        intersection1.switch_stoplights()
    intersection1.step()
    intersection1.render()
    time.sleep(0.5)
