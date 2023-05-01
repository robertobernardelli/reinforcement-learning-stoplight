from environment import *
import sys
import datetime
import time

intersection1 = Environment()

speed_up_factor = 1
#importing logs
stoplight_switches = np.load("stoplight_switches.npy", allow_pickle = True)/speed_up_factor
starting_times = np.load("starting_times.npy", allow_pickle = True)/speed_up_factor
actual_finishing_times = np.load("actual_finishing_times.npy", allow_pickle = True)/speed_up_factor

def simulation(max_speed, speed, acceleration, lookahead):
    intersection1.restart()
    switch = 0
    car_index = 0
    t = 0

    dt = datetime.datetime.now()
    
    while True:
        t += 1/32*speed_up_factor

        if t >= stoplight_switches[switch] and switch < len(stoplight_switches)-1:
            intersection1.step(switch_stoplights = True)
            switch += 1
        elif car_index < len(starting_times) and t >= starting_times[car_index]:
            intersection1.step(create_car = True, speed = speed, max_speed = max_speed, acceleration = acceleration, lookahead = lookahead)
            car_index += 1
        else:
            intersection1.step()
        
        # render only after 1/32 of a second has passed. otherwise, sleep until then
        while (datetime.datetime.now() - dt).total_seconds() < 1/32:
            print(f"only {(datetime.datetime.now() - dt).total_seconds()} seconds have passed")
            time.sleep(0.01)
        dt = datetime.datetime.now()
        intersection1.render()

    out = np.array(intersection1.average_time)/32 #no adjusting for speed up factor since the finshing times are already modified
    return out

max_speed = 1.13333
speed = 0.8
acceleration = 0.003
lookahead = 83.5714
simulation(max_speed, speed, acceleration, lookahead)