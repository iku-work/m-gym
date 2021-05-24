import gym
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from time import sleep

# Run tutorial Jib Crane model 
sim = gym.make('m_gym:wheelloader-v0')
env = DummyVecEnv([lambda: sim])

sleep(10)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=200000)

obs = env.reset()

for i in range(20000):

  sleep(1)
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)


env.close()


