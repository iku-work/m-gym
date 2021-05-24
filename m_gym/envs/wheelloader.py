import gym
from gym import spaces
import numpy as np
import os 
import sys
from m_gym.envs.createsim import CreateSimulation
from m_gym.envs.meveahandle import MeveaHandle
from time import sleep
from math import exp
#from stable_baselines.common.env_checker import check_env
import m_gym
from os import getcwd, path

class WheelLoaderEnv(gym.Env):

  def __init__(self):
    super(WheelLoaderEnv, self).__init__()

    self.config= {
    "model_name": "WheelLoader",
    "model_file_location": "\\WheelLoader",
    "debug": False,
    "episode_duration": 45,
    "excluded": ["Input_Reset"],
    "render": True, 
    "service_inputs": ["Input_Reset","Input_Ready"],
    "service_outputs": ["Output_Reset_Done"],
    "reset_input_block": 6,
    "reset_done_output_block": 0
    }
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
    
    del self.sim

  # Returns Box observation space 
  def get_observation_space(self):
    return spaces.Box(low=-np.inf, high=np.inf, shape=self.observation.shape)

  # Returns Box action space
  def get_action_space(self):
    return spaces.Box(low=self.action_low, high=self.action_high, shape=self.action.shape)

  def step(self, action):

    self.mh.set_inputs(action)

    obs = self.mh.get_outputs()
    reward = ((exp(-obs[0]) * obs[2]) +  (exp(-obs[1]) * obs[2]) + (obs[4] - obs[3]))/(obs[5] + obs[6] + obs[7] + 1)
    done = False
    
    if obs[10] >= self.config['episode_duration']:
      done = True

    return obs, reward, done, {}
  
  def reset(self):
    

    print('RESET')
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 1)
    sleep(2)
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 0)

    return 0 #self.mh.get_outputs()  # reward, done, info can't be included


  def render(self, mode='', close=False):

    pass
  
  def close(self):

    self.mh.terminate()
    self.mh.delete_folder(self.new_folder)
    print('Simulation environment closed!')
  
