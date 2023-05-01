from environment import *
<<<<<<< Updated upstream
from utils import *
=======
import datetime
import time
>>>>>>> Stashed changes

intersection1 = Intersection()

<<<<<<< Updated upstream
for timestep in range(1000):
    if timestep % 100 == 0:
        intersection1.switch_stoplights()
    intersection1.step()
    intersection1.render()
    # time.sleep(0.005)
=======
render = True
fps_limiter = True

dt = datetime.datetime.now()
for timestep in range(10000):
    if timestep % 500 == 0:
        intersection1.step(switch_stoplights = True,)
    intersection1.step()
    if render:
        if fps_limiter:
            while (datetime.datetime.now() - dt).total_seconds() < 1/32:
                time.sleep(0.01)
            dt = datetime.datetime.now()
        intersection1.render()
>>>>>>> Stashed changes
