#from .sokoban_constants import *
from .sokoban_constants import *
import os
import gym
import gym_sokoban_mod_prec
#from .CNNNetwork import Net
from .CNNNetwork import Net
import torch

# from AbstractConceptClass import AbstractConceptClass
# from constants import *
# import os
# from CNNNetwork import Net
# import torch

#'on_ladder1': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0}
prob_map = {'concept_above_switch': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_box_left': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_box_right': {'p_c_c': 0.8571428571428571, 'p_nc_nc': 1.0, 'p_nc_c': 0.1428571428571429, 'p_c_nc': 0.0},
            'concept_empty_above': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_empty_below': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_empty_left': {'p_c_c': 1.0, 'p_nc_nc': 0.9292929292929293, 'p_nc_c': 0.0, 'p_c_nc': 0.0707070707070707},
            'concept_empty_right': {'p_c_c': 1.0, 'p_nc_nc': 0.9741379310344828, 'p_nc_c': 0.0, 'p_c_nc': 0.02586206896551724},
            'concept_left_switch': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_switch_on': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_target_above': {'p_c_c': 1.0, 'p_nc_nc': 0.9964539007092199, 'p_nc_c': 0.0, 'p_c_nc': 0.0035460992907801418},
            'concept_target_below': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_target_left': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_target_right': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_wall_above': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_wall_below': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_wall_left': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_wall_left_below_ofbox': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'concept_wall_right': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0}}


class SokobanFlipConceptClass:
    def __init__(self):
        self.env = gym.make('Sokoban-mod-prec-v0')

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

    def get_all_valid_concepts(self, act_seq):
        #concepts_present = set()
        valid_concept_map = {}
        #valid_concept_map[concept] = (1, prob_map[concept]['p_nc_nc'], prob_map[concept]['p_nc_c'])
        #    else:
        #        valid_concept_map[concept] = (0, prob_map[concept]['p_c_c'], prob_map[concept]['p_c_nc'])
        state = self.env.reset()
        for act in act_seq:
            state, _, _, _ = self.env.step(act)

        for conc in CONCEPT_TO_MODEL_MAP_FOR_FLIP:
            if 'NOT_' not in conc:
                if self.run_classifier(CONCEPT_TO_MODEL_MAP_FOR_FLIP[conc], state):
                    valid_concept_map[conc] = (1, prob_map[conc]['p_nc_nc'], prob_map[conc]['p_nc_c'])
                else:
                    valid_concept_map[conc] = (0, prob_map[conc]['p_c_c'], prob_map[conc]['p_c_nc'])

        return valid_concept_map

    def save_test_imge(self, act_seq):
        #concepts_present = set()
        #valid_concept_map[concept] = (1, prob_map[concept]['p_nc_nc'], prob_map[concept]['p_nc_c'])
        #    else:
        #        valid_concept_map[concept] = (0, prob_map[concept]['p_c_c'], prob_map[concept]['p_c_nc'])
        #print (self.env.)
        state = self.env.reset()
        for act in act_seq:
            state, _, _, _ = self.env.step(act)
            print ("player_pos", self.env.player_position)
        from PIL import Image
        im = Image.fromarray(state)
        im.save("/tmp/test.png") 



if __name__ == "__main__":
    import gym
    import gym_sokoban_mod_prec
    env = gym.make('Sokoban-mod-prec-v0')
    plan = [8, 8, 8, 7, 7, 7]
    t_state = env.reset()
    t_concept_list = []
    conc_obj =SokobanFlipConceptClass()
    for t_act in plan:
        t_concept_list.append(conc_obj.get_all_concepts_for_state(t_state))
        state, reward, _ , _ = env.step(t_act)

    print (t_concept_list)

