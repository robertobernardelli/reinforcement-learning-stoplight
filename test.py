from environment import *

intersection1 = Environment()

for timestep in range(2000):
    if timestep % 100 == 0:
        intersection1.step(switch_stoplights = True)
    intersection1.step()
    intersection1.render()