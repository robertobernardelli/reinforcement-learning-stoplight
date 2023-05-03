from environment import Environment
import random
import datetime
import time
from tqdm import tqdm

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
        
render = False
dt = datetime.datetime.now()
waiting_times = []
episodes = 10
for i in tqdm(range(episodes)):
    timestep = 1
    for _ in range(32*60*15):
        if timestep % switch == 0:
            intersection1.step(switch_stoplights = True)
            change_pace(switch)
            timestep = 1
        obs = intersection1.step()
        if render:
            while (datetime.datetime.now() - dt).total_seconds() < 1/32:
                time.sleep(0.01)
            dt = datetime.datetime.now()
            intersection1.render()
        timestep += 1
    waiting_times.append(obs[0])
    intersection1.restart()

print(f'Average waiting time (over {episodes} episodes): {round((sum(waiting_times)/len(waiting_times))/32, 2)} sec')