from gym.envs.registration import register

register(
    id='wheelloader-v0',
    entry_point='m_gym.envs.wheelloader:WheelLoaderEnv'
)
