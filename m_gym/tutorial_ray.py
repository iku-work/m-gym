import gym, ray
from ray.rllib.agents import ppo
from ray.tune.registry import register_env


def env_caller(name):
  return gym.make('m_gym:wheelloader-sparse-v0')

# Run WheelLoader environment
sim = gym.make('m_gym:wheelloader-sparse-v0')
env = register_env("loader", env_caller)

ray.init()

config = ppo.DEFAULT_CONFIG.copy()
config["num_gpus"] = 0
config["num_workers"] = 3
config["num_envs_per_worker"] = 1

trainer = ppo.PPOTrainer(config=config, env="loader")

while True:
    trainer.train()

