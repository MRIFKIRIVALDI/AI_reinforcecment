import gymnasium as gym
import numpy as np
import time

env = gym.make("FrozenLake-v1", is_slippery=False)
q = np.zeros((env.observation_space.n, env.action_space.n))

alpha = 0.8
gamma = 0.95
eps = 1.0

for episode in range(1000):
    state, _=env.reset()
    done = Falsetotal_reward = 0
    total_reward = 0


    while not done:
        action = env.action_space.sample() if np.random.rand() < eps else np.argmax(q[state])
        next_state, reward, terminated, truncated, _= env.step(action)
        q[state, action] += alpha * (reward + gamma * np.max([next_state]) - q[state,action])

        state = next_state
        total_reward += reward

        done = terminated or truncated

        eps *= 0.99

        print(f"Episode {episode + 1}: Reward = {total_reward}")

env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")
state, _=env.reset()
done = False

print("\nMenjalankan demo dengan GUI...")
while not done:
    env.render()
    time.sleep(0.4)
    action = np.argmax(q[state])
    state, reward, terminated, truncated, _= env.step(action)
    done = terminated or truncated

print(f"Demo selesai! Reward: {reward}")
env.close()