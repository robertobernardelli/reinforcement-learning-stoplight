from environment import *

intersection1 = Environment()

for timestep in range(10000):
    if timestep % 100 == 0:
        intersection1.step(switch_stoplights = True)
    else:
        intersection1.step(switch_stoplights = False)
    intersection1.render()
    #time.sleep(0.0001)