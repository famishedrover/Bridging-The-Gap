import random
# from typing import List, Tuple

import gym
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd 
import torch.optim as optim

import gym_sokoban_mod

#from scipy.misc import imresize # preserves single-pixel info _unlike_ img = img[::2,::2]
from skimage.transform import resize


