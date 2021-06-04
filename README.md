# M-Gym

M-Gym is a module for using Mevea physics-based engine in reinforcement learning training. It allows to use custom simulation model of heavy machinery in Python 3. 

## Requirements
Other requirements:
- Latest Mevea Simulation Software package. For more details visit: https://mevea.com/
- Windows 10
- For installation of the M-Gym you require Python 3.7. If you want to use different version, build ```MeveaIO.pyd``` file by using this repo:  https://github.com/iku-work/MeveaIO.git and replace it at 
m-gym/m_gym/envs/. 
- For running tutorials install OpenAI Baselines: https://github.com/openai/baselines or RAY: https://docs.ray.io/en/master/index.html 

## Installation

Download and install:

```console
git clone https://github.com/iku-work/m-gym.git
pip install -e m-gym
```

