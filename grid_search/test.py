from environment import *
import pandas as pd
import numpy as np
from tqdm import tqdm

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
    time = 0

    while len(intersection1.average_time) < len(actual_finishing_times):
        time += 1/32*speed_up_factor

        if time >= stoplight_switches[switch] and switch < len(stoplight_switches)-1:
            intersection1.step(switch_stoplights = True)
            switch += 1
        elif car_index < len(starting_times) and time >= starting_times[car_index]:
            intersection1.step(create_car = True, speed = speed, max_speed = max_speed, acceleration = acceleration, lookahead = lookahead)
            car_index += 1
        else:
            intersection1.step()
        #intersection1.render()

    out = np.array(intersection1.average_time)/32 #no adjusting for speed up factor since the finshing times are already modified
    return out

def mse(actual, predicted):
    assert len(actual) == len(predicted)
    return np.mean((actual - predicted)**2)

def mae(actual, predicted):
    assert len(actual) == len(predicted)
    out = np.sort(np.abs(actual - predicted))
    return np.mean(out[:int(0.9*len(out))])

# Grid Search 1

# speeds = np.arange(0.5, 2.5, 0.5)[::-1]
# max_speeds = np.arange(0.5, 2.5, 0.5)[::-1]
# accelerations = np.arange(0.01, 0.1, 0.01)[::-1]
# lookaheads = np.arange(10, 30, 5)[::-1]

# Grid Search 2

speeds = np.arange(1.5, 5, 0.5)[::-1]
max_speeds = np.arange(2, 5, 0.5)[::-1]
acceleration = 0.03
lookaheads = np.arange(10, 30, 5)[::-1]

# Grid Search 3

# speeds = np.linspace(1, 1.5, 10)[::-1]
# max_speeds = np.linspace(1, 1.5, 10)[::-1]
# accelerations = np.linspace(0.002, 0.005, 6)[::-1]
# lookaheads = np.linspace(10, 30, 5)[::-1]

best_mae = np.inf

data = pd.DataFrame(columns = ['max_speed', 'speed', 'acceleration', 'lookahead', 'mae'])

i = 0
for j, max_speed in tqdm(enumerate(max_speeds)):
    for speed in speeds[j:]:
        #for acceleration in accelerations:
            for lookahead in lookaheads:
                #print(f'iteration: {i}')
                #print(f'config: {max_speed}, {speed}, {acceleration}, {lookahead}')
                avg_time = simulation(max_speed, speed, acceleration, lookahead)
                #mse_val = mse(starting_times + avg_time, actual_finishing_times)
                mae_val = mae(starting_times + avg_time, actual_finishing_times)
                data.loc[i] = [max_speed, speed, acceleration, lookahead, mae_val]
                #print(f'MSE: {mse_val}')
                i += 1
                if mae_val < best_mae:
                    best_mae = mae_val
                    best_speed = speed
                    best_max_speed = max_speed
                    best_acceleration = acceleration
                    best_lookahead = lookahead
                    print(f"New best MAE: {best_mae}")
                    print(f'Config: {best_max_speed}, {best_speed}, {best_acceleration}, {best_lookahead}')
                    print(actual_finishing_times-starting_times-avg_time)

data.to_csv('grid_search_macro_new.csv', index = False)