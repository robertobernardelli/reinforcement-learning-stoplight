from environment import Environment
import random
#import pygame

#set random seed
random.seed(0)

#initialize environment
intersection1 = Environment()

#set switch time
switch = 45*32

def change_pace(switch):
    if switch == 45*32:
        switch = 30*32
    else:
        switch = 45*32

#pygame.init()
#clock = pygame.time.Clock()

for i in range(2):
    timestep = 1
    for _ in range(32*60*2):
        #clock.tick(32)
        if timestep % switch == 0:
            intersection1.step(switch_stoplights = True)
            change_pace(switch)
            timestep = 1
        intersection1.step()
        intersection1.render()
        timestep += 1
    intersection1.restart()