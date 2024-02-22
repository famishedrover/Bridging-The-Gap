from .AbstractConceptClass import AbstractConceptClass
from .concept_constants import *
import os
from .CNNNetwork import Net
import torch

# from AbstractConceptClass import AbstractConceptClass
# from constants import *
# import os
# from CNNNetwork import Net
# import torch


class SokobanFlipConceptClass(AbstractConceptClass):
    def __init__(self):
        pass

    def get_all_valid_concepts(self, concept_list):
        pass

    def run_classifier(self, model_path, state):
        net = Net()
        net.load_state_dict(torch.load(model_path))
        net.eval()
        output = net(torch.tensor([state]).permute(0, 3, 1, 2).float())
        _, predicted = torch.max(output.data, 1)
        if predicted[0] != 0:
            return True
        else:
            return False

    def get_all_concepts_for_state(self, state):
        concepts_present = set()
        for conc in CONCEPT_TO_MODEL_MAP_FOR_FLIP:
            if self.run_classifier(CONCEPT_TO_MODEL_MAP_FOR_FLIP[conc], state):
                concepts_present.add(conc)
        return concepts_present

if __name__ == "__main__":
    import gym
    import gym_sokoban_mod
    env = gym.make('Sokoban-mod-v0')
    plan = [1, 1, 1, 1, 1]
    state = env.reset()
    concept_list = []
    conc_obj =SokobanFlipConceptClass()
    for act in plan:
        concept_list.append(conc_obj.get_all_concepts_for_state(state))
        state, reward, _ , _ = env.step(act)

    print (concept_list)

