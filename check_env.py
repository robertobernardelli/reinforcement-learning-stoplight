from stable_baselines3.common.env_checker import check_env
from gym_env import StoplightEnv

env = StoplightEnv(debug=True, render=False)
# It will check your custom environment and output additional warnings if needed
check_env(env)