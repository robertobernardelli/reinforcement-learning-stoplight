from environment import Environment
import random
import datetime
import time
from tqdm import tqdm

#set random seed
random.seed(0)

#initialize environment
intersection1 = Environment()
render = False
limit_fps = False

switch_seconds = range(6, 46, 1)

switch_times = [i*32 for i in switch_seconds]

waiting_times_per_switch = []

for switch in switch_times:
    print(f'Switching every {switch/32} seconds')

    
    dt = datetime.datetime.now()
    waiting_times = []
    episodes = 100
    for i in tqdm(range(episodes)):
        timestep = 1
        for _ in range(32*60*3):
            if timestep % switch == 0:
                intersection1.step(switch_stoplights = True)
                timestep = 1
            obs = intersection1.step()
            if render:
                while limit_fps and ((datetime.datetime.now() - dt).total_seconds() < 1/32):
                    time.sleep(0.01)
                dt = datetime.datetime.now()
                intersection1.render()
            timestep += 1
        waiting_times.append(obs[0])
        intersection1.restart()
    print('####')
    print(f'Switching every {switch/32} seconds:')
    print(f'Average waiting time (over {episodes} episodes): {round((sum(waiting_times)/len(waiting_times))/32, 2)} sec')
    print('####')
    waiting_times_per_switch.append((sum(waiting_times)/len(waiting_times))/32)

print('Switch Seconds:')
print(switch_seconds)

print('Waiting Times per Switch:')
print(waiting_times_per_switch)