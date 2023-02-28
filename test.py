from environment import *
from utils import *

intersection1 = Intersection()

for timestep in range(1000):
    if timestep % 100 == 0:
        intersection1.switch_stoplights()
    intersection1.step()
    intersection1.render()
    # time.sleep(0.005)
