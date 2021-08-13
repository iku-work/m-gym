import gym
from gym import spaces
import numpy as np
import os 
import sys
from m_gym.envs.createsim import CreateSimulation
from m_gym.envs.meveahandle import MeveaHandle
from time import sleep
from math import exp, sqrt


class WheelLoaderEnv(gym.Env):

  def __init__(self):
    super(WheelLoaderEnv, self).__init__()

    self.config= {
    "model_name": "WheelLoader",
    "model_file_location": "\\WheelLoader",
    "debug": False,
    "episode_duration": 45,
    "excluded": ["Input_Reset"],
    "render": False, 
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
    
    # 12, 13, 14
    #velocityBucket = sqrt(obs[12] ** 2 + obs[13] **2 + obs[14] ** 2)
    #velocityDiscount = (1 - max(velocityBucket, 0.1)^1/(max(obs[2], 0.1)))
    distanceComponent = exp(- obs[2])

    reward = distanceComponent #* velocityDiscount 

    #print("Reward: ", reward)

    done = False

    '''
    Termination states:
    - Time > episode duration
    - Time > episode duration/3 and mass in the bucket < trigger mass
    - Time > episode duration/2 and mass in the hopper < trigger mass
    '''

    if obs[10] >= self.config['episode_duration']:
      done = True
    elif obs[10] > self.config['episode_duration']/3 and obs[4] < self.bucket_trigger_mass:
      done = True
    elif obs[10] > self.config['episode_duration']/2 and obs[7] < self.dumpster_trigger_mass:
      done = True

    return obs, reward, done, {}


  def reset(self):
    
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 1)
    sleep(2)
    self.mh.set_single_digital_input(self.config['reset_input_block'], self.mh.worker_number, 0)

    return self.mh.get_outputs()

  def render(self, mode='', close=False):
    pass
  
  def close(self):
    
    self.mh.terminate()
    self.mh.delete_folder(self.new_folder)
    print('Simulation environment closed!')
  
