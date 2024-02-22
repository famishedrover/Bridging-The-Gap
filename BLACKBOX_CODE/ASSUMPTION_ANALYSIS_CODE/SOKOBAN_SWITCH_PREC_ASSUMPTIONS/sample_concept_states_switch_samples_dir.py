import random
# from typing import List, Tuple
import pickle
import gym
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd 
import torch.optim as optim

import gym_sokoban_mod_prec
# import gym_sokoban_flip_mod 

from constt import *
import copy

import utils
import logics

import os

import pprint 




# ROOT = "runs-flip"

#from scipy.misc import imresize # preserves single-pixel info _unlike_ img = img[::2,::2]
# 
# --- Find all concepts
allConceptsFuncs = utils.findAllConcepts()

# resfunc = getattr(logics, 'concept_box_below')

utils.createDirs(allConceptsFuncs,ROOT=ROOT)


ACTION_LOOKUP = {
0: "no operation",
1: "push up",
2: "push down",
3: "push left",
4: "push right",
5: "move up",
6: "move down",
7: "move left",
8: "move right",
}


env_name = 'Sokoban-mod-prec-v0'

#env_name = 'Sokoban-mod-v0'
# env_name = 'Sokoban-mod-flip-v0'
env = gym.make(env_name) ; 



env.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)


# ------- CODE STARTS HERE -----







# since neg are ALOT we can take only 10% of those....


def randomStartAgent(env, STEP_LIMIT=20):
    # 

    curr_seq = []
    plan = [8, 8, 8, 7, 7, 7,1,1,1,1]
    max_step = random.randint(0,len(plan)-1)
    # read the prioritydqn agent for this map & run according to its policy 
    for action in plan[:max_step]:
        # state = env.room_state
        state = env.render(mode="rgb_array")
        env.step(action)
        curr_seq.append(action)

    return env, curr_seq



def sample_states(env, eps, iters, randomStart=False, render=True, traceheatMap=True):

    state_hash = set()


    logger = {}
    playerMask, boxMask = logics.getMask(env.room_state)


    # idx 0 is pos, idx 1 is neg, idx 2 is ACTUTAL_NEG
    POSIDX = 0
    NEGIDX = 1
    AC_NEGIDX = 2
    for concept in allConceptsFuncs : 
        logger[concept] = [0,0,0]


    sample_id = 0
    for ep in range(eps):

        env.reset()

        print ("ep[",ep,"/",eps,"]", "  Count pos/neg/actualneg")
        pprint.pprint(logger)

        utils.saveMasks(playerMask, boxMask, ROOT, ep)
        action_seq = []
        if randomStart :
            env, curr_seq = randomStartAgent(env, STEP_LIMIT=20)
            action_seq = copy.deepcopy(curr_seq)
        for i in range(iters):
            action = random.randint(0,8) 
            action_seq.append(action)
            # action = int(input())
            state, reward, done, _ = env.step(action)
            img = env.render(mode="rgb_array")


            if done : 
                break
            sample_name = "sample_"+str(sample_id)
            path = ROOT+"/samples"
            path_image = path + "/"+sample_name+".png"
            path_seq = path + "/"+sample_name+".seq"
            # save for pos
            utils.save_img(img, path_image)
            with open(path_seq, 'wb') as p_fd:
                 pickle.dump(action_seq, p_fd)
            #ddfiltered_concept_map[conc] = logger[conc]
            sample_id += 1


sample_states(env, eps=1000, iters=120, randomStart=True)
















