# Traffic Control with Reinforcement Learning

The objective of the agent is to control the four stoplights of the intersection and minimize the waiting times. Built with Stable Baselines 3 and OpenAI Gym.

![stoplight ai](simulation.gif)

 The environment is defined in `gim_env.py`. The model used is PPO (Proximal Policy Optimization)

The agent has two actions:
* Switch the stoplights
* Do nothing

The agent performs an action every 10 seconds of simulation. Every time a switch is performed, stoplights all go red for 5 seconds (like in the real world)

The observation includes:
* Number of cars waiting that come from North + South
* Number of cars waiting that come from East + West
* Boolean to keep track what direction is currently flowing
* Number of steps since last switch

The reward function is simply defined as follows:

`reward = -(n_waiting_cars^2)`

- `n_waiting_cars`: total number of waiting cars (North + East + South + West)

## Setup

`$ pip install -r requirements.txt`

## Usage

To run the pretrained model, simply execute this command:

`$ python3 test_rl_best.py`

To run the current real world configuration (no Reinforcement Learning), run:

`$ python3 test_environment.py`