import gym
import gym_sokoban_mod
import matplotlib.pyplot as plt
import numpy as np
import os
import pprint
import random
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.functional as F
import torch.optim as optim
import torch.optim as optim

import concept_utils
import utils
from CNNNetwork import Net
from local_constants import *

# from typing import List, Tuple
# import gym_sokoban_flip_mod


# ROOT = "runs-flip"

#from scipy.misc import imresize # preserves single-pixel info _unlike_ img = img[::2,::2]
#
# --- Find all concepts
allConceptsFuncs = list(concept_utils.CONCEPT_TO_MODEL_MAP.keys())

# resfunc = getattr(logics, 'concept_box_below')

#utils.createDirs(allConceptsFuncs,ROOT=ROOT)


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



env_name = 'Sokoban-mod-v0'
env = gym.make(env_name)

seed = 20

env.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)


# ------- CODE STARTS HERE -----


SOKOBAN_SWITCH_DATA = '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_SAMPLES_APR_23'

CONCEPT_MAP_FILE_NAME_PREFIX = 'CONCEPT_MAP'

EMPTY_CONCEPTS = 'ALL'

# since neg are ALOT we can take only 10% of those....


def randomStartAgent(env, STEP_LIMIT=20):
    foil = [1,1,1,1]
    curr_steps = random.randint(0, len(foil))
    # Pick a state from the foil plan
    for step in foil[:curr_steps]:
        # state = env.room_state
        env.step(step)
    return env



def sample_states(env, eps, iters, randomStart=False, render=True, traceheatMap=True):
    curr_id = 0
    state_hash = set()
    concept_map = {}
    concept_map[EMPTY_CONCEPTS] = set()


    for ep in range(eps):

        env.reset()

        curr_plan = []

        if randomStart :
            env = randomStartAgent(env, STEP_LIMIT=20)

        for i in range(iters):
            action = random.randint(0,8)
            curr_plan.append(action)
            # action = int(input())
            next_, reward, done, _ = env.step(action)

            if render:
                env.render()
            img = env.render(mode="rgb_array")

            state = env.room_state
            # if state is already visited then skip the concept step ....


            if hash(state.tostring()) in state_hash :
                print ("Same found")

                # we can maybe do away with else by just continue,-- but there's a done at the bottom which needs to be taken care of...
            else :
                print ("New")
                concept_map[EMPTY_CONCEPTS].add(curr_id)
                state_hash.add(hash(state.tostring()))
                path = SOKOBAN_SWITCH_DATA + "/"
                img_path = path + "state" + str(curr_id) + "_img.png"
                seq_path = path + "state" + str(curr_id) + "_seq.png"

                # save for pos
                utils.save_img(img, img_path)
                with open(seq_path, 'w') as p_fd:
                    p_fd.write("\n".join([str(i) for i in curr_plan]))

                for concept in allConceptsFuncs:
                    #func = getattr(logics, concept)
                    neg_concept = "NOT_" + concept
                    label = concept_utils.run_classifier(concept, img)
                    print ("label")
                    if label:
                        if concept not in concept_map:
                            concept_map[concept] = set()
                        concept_map[concept].add(curr_id)
                    else:
                        # Put it into neg
                        if neg_concept not in concept_map:
                            concept_map[neg_concept] = set()
                        concept_map[neg_concept].add(curr_id)
                curr_id += 1

            if done :
                break

    allConceptsFuncs.append(EMPTY_CONCEPTS)
    for conc in allConceptsFuncs:
        neg_concept = "NOT_" + conc
        if conc in concept_map:
            with open(SOKOBAN_SWITCH_DATA +"/"+ CONCEPT_MAP_FILE_NAME_PREFIX+ "/"+conc, 'w') as p_fd:
                p_fd.write("\n".join([str(i) for i in list(concept_map[conc])]))
        if neg_concept in concept_map:
            with open(SOKOBAN_SWITCH_DATA +"/"+ CONCEPT_MAP_FILE_NAME_PREFIX+ "/"+neg_concept, 'w') as p_fd:
                p_fd.write("\n".join([str(i) for i in list(concept_map[neg_concept])]))

#sample_states(env, eps=1000, iters=120, randomStart=False)

sample_states(env, eps=10000, iters=120, randomStart=True)














