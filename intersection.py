import gym
from gym import spaces
import numpy as np
import cv2
from utils import *


class IntersectionEnv(gym.Env):
    def __init__(self):
        super(IntersectionEnv, self).__init__()
        self.action_space = spaces.Discrete(3)  # 0: left, 1: right, 2: no action
        # these low and high parameters are for sanity check, they could be np.inf and -np.inf
        # the shape is the number of inputs in the observation space
        self.observation_space = spaces.Box(
            low=-1000, high=1000, shape=(5,), dtype=np.float32
        )

    def render(self):
        cv2.imshow("SailingEnv", self.img)
        cv2.waitKey(1)

        # initialize map and dashboard
        self.img = draw_sea_and_dashboard(
            self.wind_direction, self.boat_heading, self.boat_speed, self.total_reward
        )

        step()

    def step(self, action):
        """
        Take an action and return the new state, reward, and done
        """

        button_direction = action

        # decode action
        if button_direction == 1:
            self.boat_heading += 10
        elif button_direction == 0:
            self.boat_heading -= 10

        # update internal state
        # ...

        # reward function
        self.total_reward = (
            (250 - euclidean_dist_to_target) + target_reward - 2 * self.time
        ) / 100

        # create observation:
        observation = [
            #
            # N of cars waiting in A
            # N of cars waiting in B
            # ...
        ]
        observation = np.array(observation).astype("float32")

        info = {}

        self.time += 1

        return observation, self.total_reward, self.done, info

    def reset(self):
        """
        Reset the environment to the initial state
        (including the image)
        """

        self.done = False

        self.time = 0

        self.img = np.zeros((600, 900, 3), dtype="uint8")

        # create observation:
        observation = [
            #
            # N of cars waiting in A
            # N of cars waiting in B
            # ...
        ]
        observation = np.array(observation).astype("float32")

        return observation
