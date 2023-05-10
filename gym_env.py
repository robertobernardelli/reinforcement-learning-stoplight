import gym
from gym import spaces
import numpy as np
from environment import Environment
import datetime 
import time


class StoplightEnv(gym.Env):
    def __init__(self, render=False, debug=False, limit_fps=False):
        super(StoplightEnv, self).__init__()
        
        self.intersection = Environment()
        
        self.action_space = spaces.Discrete(2)  # 0: no action, 1: switch stoplights
        
        # these low and high parameters are for sanity check, they could be np.inf and -np.inf
        # the shape is the number of inputs in the observation space
        self.observation_space = spaces.Box(
            low=-1000, high=1000, shape=(4,), dtype=np.float32
        )
        
        self.render_required = render
        self.debug_required = debug
        self.limit_fps = limit_fps
        
        self.stoplight_switched = False
        self.steps_since_last_switch = 0

    def render(self):
        
        if self.render_required:
            
            if self.limit_fps:
                while (datetime.datetime.now() - self.dt).total_seconds() < 1/32:
                    time.sleep(0.01)
            
                self.dt = datetime.datetime.now()
                
            self.intersection.render()

    def step(self, action):

        switch_stoplight = action  # 0: no action, 1: switch stoplights

        if self.debug_required:
            print(f'Action: {switch_stoplight}')
        
        if switch_stoplight == 0 or self.steps_since_last_switch < (32*5):
            obs = self.intersection.step(switch_stoplights=False)
            self.render()
            self.time += 1
            self.steps_since_last_switch += 1
            
        else: # switch_stoplight == 1 and self.steps_since_last_switch >= (32*5)
            obs = self.intersection.step(switch_stoplights=True)
            self.stoplight_switched = not self.stoplight_switched
            self.steps_since_last_switch = 0
            self.render()
            self.time += 1
            
        # The agent needs to wait for 1 second before doing another action
        for _ in range(10*32-1): # 1 seconds = 32 timesteps (minus 1 because we already did 1 step above)
            obs = self.intersection.step(switch_stoplights=False)
            self.render()
            self.time += 1
            self.steps_since_last_switch += 1

        avg_waiting_time = obs[0]

        self.total_reward = -avg_waiting_time

        waiting_cars0 = obs[1]
        waiting_cars1 = obs[2]
        waiting_cars2 = obs[3]
        waiting_cars3 = obs[4]
        
        # merging to help the agent learn faster
        waiting_north_south = waiting_cars0 + waiting_cars1
        waiting_east_west = waiting_cars2 + waiting_cars3
        
        # create observation:
        observation = [
            waiting_north_south,
            waiting_east_west,
            self.stoplight_switched,
            self.steps_since_last_switch
        ]

        info = {'average_waiting_time': avg_waiting_time}

        if self.time > 32*60*10:
            self.done = True


        return observation, self.total_reward, self.done, info

    def reset(self):
        
        self.intersection.restart()
        
        self.stoplight_switched = False
        self.steps_since_last_switch = 0
        
        self.dt = datetime.datetime.now()

        self.done = False

        self.time = 0

        waiting_cars0 = 0
        waiting_cars1 = 0
        waiting_cars2 = 0
        waiting_cars3 = 0
        
        # merging to help the agent learn faster
        waiting_north_south = waiting_cars0 + waiting_cars1
        waiting_east_west = waiting_cars2 + waiting_cars3
        
        # create initial observation:
        observation = [
            waiting_north_south,
            waiting_east_west,
            self.stoplight_switched,
            self.steps_since_last_switch
        ]
        
        observation = np.array(observation).astype("float32")

        return observation
