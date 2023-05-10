import gym
from gym_env import StoplightEnv
from tqdm import tqdm
from stable_baselines3 import PPO

def main():

    env = StoplightEnv(render=False, debug=False, limit_fps=False)
    env.reset()

    model_path = "models/1683139451/5800.zip"
    model = PPO.load(model_path, env=env)
    
    episodes = 10

    waiting_times = []
    
    for ep in tqdm(range(episodes)):
        obs = env.reset()
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            print(rewards)
        waiting_times.append(info['average_waiting_time'])
    env.close()
    
    print(f'Average waiting time (over {episodes} episodes): {round((sum(waiting_times)/len(waiting_times))/32, 2)} sec')

if __name__ == "__main__":
    main()
