from environment import *
import datetime
import time

intersection1 = Environment()

render = False
fps_limiter = False

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
