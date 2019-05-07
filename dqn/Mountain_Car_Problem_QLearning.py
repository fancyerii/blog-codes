# coding: utf-8


# Q-Learning example using OpenAI gym MountainCar environment

import gym
import numpy as np

n_states = 40
episodes = 10  # number of episodes

initial_lr = 1.0  # Learning rate
min_lr = 0.005
gamma = 0.99
max_steps = 300
epsilon = 0.05

# exploring Mountain Car environment

env_name = 'MountainCar-v0'
env = gym.make(env_name)

# One-dimensional discrete action space.
# left,neutral,right
print("Action Set size :", env.action_space)

# Two-dimensional continuous state space.
# Velocity=(-0.07,0.07)
# Position=(-1.2,0.6)
print("Observation set shape :", env.observation_space)  # 2 (position,velocity)
print("Highest state feature value :", env.observation_space.high)  # i.e. (position = 0.6, velocity = 0.07)
print("Lowest state feature value:", env.observation_space.low)  # (position = -1.2, velocity = -0.07)
print(env.observation_space.shape)  # 2


# Discretization of continuous state space : Converting continuous state space observation to a discrete set of state space

def discretization(env, obs):
    env_low = env.observation_space.low
    env_high = env.observation_space.high

    env_den = (env_high - env_low) / n_states
    pos_den = env_den[0]
    vel_den = env_den[1]

    pos_high = env_high[0]
    pos_low = env_low[0]
    vel_high = env_high[1]
    vel_low = env_low[1]

    pos_scaled = int((obs[0] - pos_low) / pos_den)
    vel_scaled = int((obs[1] - vel_low) / vel_den)

    return pos_scaled, vel_scaled


env = env.unwrapped
env.seed(0)
np.random.seed(0)
# Q table
# rows are states but here state is 2-D pos,vel
# columns are actions
# therefore, Q- table would be 3-D

q_table = np.zeros((n_states, n_states, env.action_space.n))
total_steps = 0
for episode in range(episodes):
    obs = env.reset()
    total_reward = 0
    # decreasing learning rate alpha over time
    alpha = max(min_lr, initial_lr * (gamma ** (episode // 100)))
    steps = 0
    while True:
        env.render()
        pos, vel = discretization(env, obs)

        if np.random.uniform(low=0, high=1) < epsilon:
            a = np.random.choice(env.action_space.n)
        else:
            a = np.argmax(q_table[pos][vel])

        obs, reward, terminate, _ = env.step(a)
        # 对reward进行优化
        # reward = -10 + abs(obs[0] + 0.5)
        # q-table update
        pos_, vel_ = discretization(env, obs)
        q_table[pos][vel][a] = (1 - alpha) * q_table[pos][vel][a] + alpha * (
                reward + gamma * np.max(q_table[pos_][vel_]))
        steps += 1
        if terminate:
            break
    print("Episode {} completed with total reward {} in {} steps".format(episode + 1, total_reward, steps))

while True:  # to hold the render at the last step when Car passes the flag
    env.render()
