import gym
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from time import sleep

# Run WheelLoader environment
sim = gym.make('m_gym:wheelloader-v0')
env = DummyVecEnv([lambda: sim])

# Wait till Mevea Solver opens
sleep(10)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=200000)

# Reset an environment
obs = env.reset()

for i in range(20000):
  
  # Skip frame
  sleep(1)
  
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)

env.close()


