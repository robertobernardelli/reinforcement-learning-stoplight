import gym
from gym_env import StoplightEnv
from tqdm import tqdm

def main():

    env = StoplightEnv(render=False, debug=True)
    env.reset()

    episodes = 10

    waiting_times = []
    
    for ep in tqdm(range(episodes)):
        obs = env.reset()
        done = False
        while not done:
            action = 1
            obs, rewards, done, info = env.step(action)
            print(obs)
        waiting_times.append(info['average_waiting_time'])
    env.close()
    
    print(f'Average waiting time (over {episodes} episodes): {round((sum(waiting_times)/len(waiting_times))/32, 2)} sec')

if __name__ == "__main__":
    main()
