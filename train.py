from stable_baselines3 import PPO
import os
from gym_env import StoplightEnv
import time


def calculate_average_reward(model, env, num_episodes=1):
    total_reward = 0
    for i in range(num_episodes):
        obs = env.reset()
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, reward, done, _info = env.step(action)
            total_reward += reward
    return total_reward / num_episodes


models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = StoplightEnv(debug=False, render=False)
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, n_steps = 2048)

TIMESTEPS = 2048*10 # every 10 internal state updates, we save the model
iters = 0
best_average_reward = -float("inf")
while True:
    iters += 1
    model.learn(
        total_timesteps=TIMESTEPS, tb_log_name=f"PPO", progress_bar=True
    )

    print(f"Learning finished, total timesteps: {TIMESTEPS}")
    print('Starting evaluation of model')
    # Calculate average reward over some number of episodes
    avg_reward = calculate_average_reward(model, env, num_episodes=3)
    model.save(f"{models_dir}/{TIMESTEPS*iters}")

    if avg_reward > best_average_reward:
        best_average_reward = avg_reward
        model.save(f"{models_dir}/best")
        print(f"SAVED BEST MODEL {avg_reward}")
    