import gym
from gym import spaces
import numpy as np
import os 
import sys
from m_gym.envs.createsim import CreateSimulation
from m_gym.envs.meveahandle import MeveaHandle
from time import sleep
from math import exp


class ExcavatorDiggingSparseEnv(gym.Env):

  def __init__(self):
    super(ExcavatorDiggingSparseEnv, self).__init__()

    self.config= {
    "model_name": "Excavator",
    "model_file_location": "Excavator",
    "debug": False,
    "episode_duration": 45,
    "excluded": ["Input_Reset"],
    "render": True, 
    "service_inputs": ["Input_Reset","Input_Ready"],
    "service_outputs": ["Output_Reset_Done"],
    "reset_input_block": 12,
    "reset_done_output_block": 1,

    }
    #"workers_directory":"..\\Workers"

    self.sim = CreateSimulation(self.config)
    self.new_folder = self.sim.new_folder
    self.model_file_path = self.sim.model_file_path

    # Get amount of the parameters in the observation vector
    self.obs_len = self.sim.observation_len
    
    # Get amount of the parameters in the action vector
    self.act_len = self.sim.action_len

    # Create observation and action numpy array
    self.observation = np.zeros(self.obs_len, dtype=np.float32)
    self.action = np.zeros(self.act_len, dtype=np.float32)
    self.action_high = np.ones(self.act_len, dtype=np.float32)
    self.action_low = -self.action_high 
    
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self.observation.shape)
    self.action_space = spaces.Box(low=self.action_low, high=self.action_high, shape=self.action.shape)

    self.mh = MeveaHandle(self.sim.worker_number, self.sim.analog_inputs_blocks , self.sim.digital_inputs_blocks, self.sim.analog_outputs_blocks, self.sim.digital_outputs_blocks)
    self.mh.start_process(os.path.abspath(self.model_file_path), self.config['render'])
    

    self.bucket_trigger_mass = 100
    self.dumpster_trigger_mass = 100

    del self.sim

  # Returns Box observation space 
  def get_observation_space(self):
    return spaces.Box(low=-np.inf, high=np.inf, shape=self.observation.shape)

  # Returns Box action space
  def get_action_space(self):
    return spaces.Box(low=self.action_low, high=self.action_high, shape=self.action.shape)

  def step(self, action):

    self.mh.set_inputs(action)
    sleep(1)
    obs = self.mh.get_outputs()
    print(self.get_action_space())
    reward = 1
    done = False

    print(obs[11], obs[11] >= self.config['episode_duration'])

    if obs[11] >= self.config['episode_duration']:
      done = True

    return obs, reward, done, {}
  
  def reset(self):
    '''
    print("restart")
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 1)
    sleep(1)
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 0)

    obs = self.mh.get_outputs()

    while round(obs[11]) != 0: 
      self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 0)
      obs = self.mh.get_outputs()
      sleep(0.1)
    '''
    return self.mh.get_outputs()

  def render(self, mode='', close=False):
    pass
  
  def close(self):
    
    self.mh.terminate()
    self.mh.delete_folder(self.new_folder)
    print('Simulation environment closed!')
  
