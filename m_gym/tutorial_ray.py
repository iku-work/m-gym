import gym, ray
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray import tune

import sys,os
from os import getcwd, path, makedirs, listdir
import m_gym.envs.createsim as create_sim
from shutil import rmtree



def env_caller(name):
  return gym.make('m_gym:wheelloader-dense-v0')

workers_dir = path.dirname(path.abspath(create_sim.__file__)) + "\\Workers"

# Run WheelLoader environment
env = register_env("loader", env_caller)

ray.init()

config = ppo.DEFAULT_CONFIG.copy()
config["num_gpus"] = 1
config["num_workers"] = 4
config["num_envs_per_worker"] = 1

trainer = ppo.PPOTrainer(config=config, env="loader")


while True:

  try:

    trainer.train()

  except KeyboardInterrupt:
    print("Saving checkpoints")


'''

tune.run(
    "PPO",
    stop={"episode_reward_mean": 0.02},
    config={
        "env": "loader",
        "num_gpus": 0,
        "num_workers": 1,
        "lr": tune.grid_search([0.01, 0.001, 0.0001]),
    },
)


'''