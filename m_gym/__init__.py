from gym.envs.registration import register

register(
    id='wheelloader-dense-v0',
    entry_point='m_gym.envs.wheelloader:WheelLoaderEnv'
)

register(
    id='wheelloader-sparse-v0',
    entry_point='m_gym.envs.wheelloader_sparse:WheelLoaderSparseEnv'
)

register(
    id='excavator-digging-sparse-v0',
    entry_point='m_gym.envs.excavator_digging_sparse:ExcavatorDiggingSparseEnv'
)