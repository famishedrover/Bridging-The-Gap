#from Search import BreadthFirstSearch
from constants import *
import os
import copy
import yaml
import time
import pickle
from pydoc import locate

#SAMPLES_DIR = "../DATA/SAMPLES/MONTEZUMAL3/"
SAMPLES_DIR = "/tmp/sokoban_switch_samples/"
RAM_NAME = "sample_RAM.b"
ACTION_SEQ = "sample_action_seq.b"

# PROB_MAP = {'onLadderTop': {'p_nc_c': 0.00645, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 0.99355},
#             'inAir': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
#             'isClearUpCrab': {'p_nc_c': 0.00968, 'p_nc_nc': 0.99661, 'p_c_nc': 0.00339, 'p_c_c': 0.99032},
#             'crabLiesToRight': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
#             'isClearDownCrab': {'p_nc_c': 0.00645, 'p_nc_nc': 0.99322, 'p_c_nc': 0.00678, 'p_c_c': 0.99354},
#             'onLadderBottom': {'p_nc_c': 0.0, 'p_nc_nc': 0.99492, 'p_c_nc': 0.00508, 'p_c_c': 1.0},
#             'crabLiesToLeft': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
#             'onLadder': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
#             'onLeftPassage': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
#             'onRightPassage': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0}}

# PROB_MAP = {'on_ladder1': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'on_ladder2': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'on_ladder3': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'on_highest_platform': {'p_c_c': 1.0, 'p_nc_nc': 0.9982638888888888, 'p_nc_c': 0.0, 'p_c_nc': 0.001736111111111111},
#             'on_rope': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'on_ground_and_alive': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'skull_on_right': {'p_c_c': 0.75, 'p_nc_nc': 0.9938271604938271, 'p_nc_c': 0.25, 'p_c_nc': 0.006172839506172839},
#             'skull_on_left': {'p_c_c': 0.8662790697674418, 'p_nc_nc': 0.9940298507462687, 'p_nc_c': 0.13372093023255813, 'p_c_nc': 0.005970149253731343},
#             'on_middle_platform': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
#             'die_on_left': {'p_c_c': 1.0, 'p_nc_nc': 0.9906542056074766, 'p_nc_c': 0.0, 'p_c_nc': 0.009345794392523364}}

PROB_MAP = {'concept_above_switch': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
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


class ConceptLattice:
    def __init__(self, foil_act, curr_state = None, domain_name = None, starting_concepts=None, prob_dist=None):
        self.original_distribution = {}
        for conc in prob_dist:
            self.original_distribution[conc] = prob_dist[conc]
            self.original_distribution[NEG_CONCEPT_PREFIX+conc] = 1 - prob_dist[conc]
        self.curr_state = curr_state
        self.foil_act = foil_act
        self.domain_name = domain_name
        # Load the hash dict file
        print ("Loading Hash....")
        #with open(hash_dict_file) as h_fd:
        #    self.hash_dict = yaml.load(h_fd)
        # Load all possible concepts
        print ("Finished Loading Hash....")
#        self.concept_list = []
#        for i in self.hash_dict.keys():
#            if i != ALL_FILES and i != STR_SEQ_MAP and i != STR_CONC_MAP:
#                self.concept_list.append(i)
        if domain_name == 'montezuma':
            #self.concept_list = ['door_on_right_position','has_key','holding_on_to_the_rope_bottom','holding_on_to_the_rope_top','key_above','key_on_left','key_on_right','on_ground_and_alive','on_highest_platform','on_ladder1','on_ladder2','on_ladder3','on_middle_platform','on_rope','skull_on_left','skull_on_right','wall_on_left','wall_on_right', 'die_on_left']
            self.concept_list = ['on_ladder1', 'on_ladder2', 'on_ladder3', 'on_highest_platform', 'on_rope', 'on_ground_and_alive', 'on_middle_platform', 'die_on_left', 'skull_on_left', 'skull_on_right']
        elif domain_name == 'montezumal3':
            self.concept_list = ["onLadder","inAir",
                             "isClearDownCrab","isClearUpCrab","crabLiesToRight",
                            "crabLiesToLeft",
                                 "onLadderBottom",
                             "onLadderTop","onLeftPassage","onRightPassage"]
        elif domain_name == 'sokoban_flip_prec':
            self.concept_list = ['concept_above_switch','concept_box_left',
                            'concept_box_right','concept_empty_above','concept_empty_below','concept_empty_left',
                            'concept_empty_right','concept_left_switch','concept_switch_on','concept_target_above',
                            'concept_target_below','concept_target_left','concept_target_right','concept_wall_above',
                            'concept_wall_below','concept_wall_left_below_ofbox','concept_wall_left','concept_wall_right']
        print ("Created concept list")
        # Make the simulator obj
        self.simulator_obj = locate(SIMULATOR_CLASS_MAP[self.domain_name])()
        # Make the ConceptClassifierClass obj
        self.class_obj = locate(CONCEPT_CLASS_MAP[self.domain_name])()

        if curr_state:
            self.starting_concepts = self.class_obj.get_all_valid_concepts(curr_state)
        elif starting_concepts:
            self.starting_concepts = starting_concepts

    def get_successors(self, node):
        pos_concepts, neg_concept = node[0]
        successor_nodes = []
        for conc in self.concept_list | (self.starting_concepts | pos_concepts | neg_concept):
            new_pos_concepts = pos_concepts | set([conc])
            new_neg_concepts = neg_concept | set([conc])
            successor_nodes.append([(new_pos_concepts, neg_concept)])
            successor_nodes.append([(pos_concepts, new_neg_concepts)])
        return successor_nodes
    
    def get_states_without_concepts(self, pos_concepts=set(), neg_concepts=set()):
        resultant_states = set()
        if len(neg_concepts) > 0:
            resultant_states = self.hash_dict[list(neg_concepts)[0]]
            for conc in neg_concepts:
                resultant_states  &= self.hash_dict[conc]
        elif len(pos_concepts) > 0:
            resultant_states = self.hash_dict[ALL_FILES] - self.hash_dict[list(pos_concepts)[0]]
        for conc in pos_concepts:
            resultant_states  &= self.hash_dict[ALL_FILES] - self.hash_dict[conc]
        return resultant_states      

    def test_action_in_all_state(self, node):
        pos_concepts, neg_concepts = node[0]
        if len(pos_concepts) + len(neg_concepts) == 0:
            return True
        all_alt_states = self.get_states_without_concepts(pos_concepts, neg_concepts)
        for state in all_alt_states:
            act_status, next_state = self.simulator_obj.test_action(self.hash_dict[STR_SEQ_MAP][state], self.foil_act)
            if ABSOLUTE_TEST:
                if not act_status:
                    return False
        return True 

    def test_action_in_curr_state(self, state):
        act_status, next_state = self.simulator_obj.test_action(self.hash_dict[STR_SEQ_MAP][state], self.foil_act)
        if ABSOLUTE_TEST:
            if not act_status:
                return False
        return True


    def test_action_in_curr_state_from_seq(self, act_seq):
        #print ("test", self.foil_act)
        act_status = self.simulator_obj.test_action(act_seq, self.foil_act)
        if ABSOLUTE_TEST:
            if not act_status:
                return False
        return True


    def conditional_on_not_prec(self, p_no_c, p_no_nc, p_c_in_s):
        return (p_no_c * p_c_in_s) + (p_no_nc * (1 - p_c_in_s))

    def conditional_on_prec(self, p_no_c, p_no_nc):
        return (p_no_nc * 0) + (p_no_c * 1)

    def posterior_prob(self, prior_on_c_in_prec, p_no_c, p_no_nc, p_c_in_s):
        numer = self.conditional_on_not_prec(p_no_c, p_no_nc, p_c_in_s)*(1 - prior_on_c_in_prec)

        #numer = obs_prob * (1 - curr_prob)
        denom = self.conditional_on_not_prec(p_no_c, p_no_nc, p_c_in_s)*(1 - prior_on_c_in_prec) + self.conditional_on_prec(p_no_c, p_no_nc)*prior_on_c_in_prec

        #print ("Of not being in precondition", numer/denom)
        return (1 -  (numer/denom))

    def get_updated_probs(self, remaining_concept, current_probs, obs_prob):

        updated_prob = {}
        for conc in obs_prob:
            if conc in remaining_concept:
                # This is an instance of a positive observation

                #updated_prob[conc] = self.posterior_prob(current_probs[conc], obs_prob[conc], self.original_distribution[conc])
                # Test pass
                conc_dist = self.original_distribution[conc]
                if conc in PROB_MAP:
                    p_no_c = PROB_MAP[conc]['p_c_c']
                    p_no_nc = PROB_MAP[conc]['p_nc_c']
                else:
                    p_no_c = PROB_MAP[conc.replace(NEG_CONCEPT_PREFIX,'')]['p_nc_nc']
                    p_no_nc = PROB_MAP[conc.replace(NEG_CONCEPT_PREFIX,'')]['p_c_nc']
                #updated_prob[conc] = current_probs[conc]
                updated_prob[conc] = self.posterior_prob(current_probs[conc], p_no_c, p_no_nc, conc_dist)
                #self.posterior_prob(current_probs[conc], obs_prob[conc],
                                                         #self.original_distribution[conc])
                #print ("Adding concept ", conc, updated_prob[conc])
            else:

                if NEG_CONCEPT_PREFIX in conc:
                    opp_concept = conc.replace(NEG_CONCEPT_PREFIX, '')
                else:
                    opp_concept = NEG_CONCEPT_PREFIX + conc

                if opp_concept in self.original_distribution:
                    conc_dist = self.original_distribution[opp_concept]
                else:
                    conc_dist = 1 - self.original_distribution[opp_concept.replace(NEG_CONCEPT_PREFIX, '')]

                #print ("Checking obs prob for", opp_concept, conc_dist, obs_prob[conc])

                p_no_nc, p_no_c = obs_prob[conc]

                if opp_concept in remaining_concept:
                    # This is an instance of a negative observation
                    updated_prob[opp_concept] = self.posterior_prob(current_probs[opp_concept], p_no_c, p_no_nc, conc_dist)

                    #print ("Adding concept ", opp_concept, updated_prob[opp_concept])
        return updated_prob

    def get_state_concepts(self, state):
        pos_concepts = self.hash_dict[STR_CONC_MAP][state]
        neg_concepts = set()
        for conc in set(self.concept_list) -  pos_concepts:
            neg_concepts.add(NEG_CONCEPT_PREFIX + conc)
        return pos_concepts | neg_concepts

    def get_state_concepts_from_classifier_with_prob(self, state):
        full_concept_map = {}

        concepts_map_tuple = self.class_obj.get_all_valid_concepts(state)

        for conc in concepts_map_tuple:
            label, prob, prob_neg = concepts_map_tuple[conc]
            print ("entry", label, prob, prob_neg)
            if label == 1:
                full_concept_map[conc] = (prob, prob_neg)
            else:
                full_concept_map[NEG_CONCEPT_PREFIX + conc] = (prob, prob_neg)
        return full_concept_map


    def search_from_files(self):
        CURR_POSS_CONCEPTS = set()

        CURR_POSS_CONCEPTS_MAP = {}

        self.sample_count_map = {}

        # Assuming starting concepts are known with confidence
        for concept in set(self.concept_list) - set(self.starting_concepts):
            CURR_POSS_CONCEPTS.add(concept)
            CURR_POSS_CONCEPTS_MAP[concept] = 0.5
            #self.sample_count_map[concept]['pos'] = 0
            #self.sample_count_map[concept]['neg'] = 0

        for concept in self.starting_concepts:
            CURR_POSS_CONCEPTS.add(NEG_CONCEPT_PREFIX + concept)
            CURR_POSS_CONCEPTS_MAP[NEG_CONCEPT_PREFIX + concept] = 0.5
            #self.sample_count_map[NEG_CONCEPT_PREFIX + concept]['pos'] = 0
            #self.sample_count_map[NEG_CONCEPT_PREFIX + concept]['neg'] = 0


        states_covered = set()
        print ("Starting Concepts", CURR_POSS_CONCEPTS)
        sample_cnt = 0
        for root, dirs, files in os.walk(SAMPLES_DIR):
            for sfile in files:
                #sdir="38904"
                #sdir="103632"
                #sdir="65151"
                sample_cnt +=1
                print ("Checking directory ...",sfile)
                print ("Current distribution:", CURR_POSS_CONCEPTS_MAP)

                #states_covered.add(sdir)
                current_sample_file = os.path.join(SAMPLES_DIR, sfile)

                with open(current_sample_file, 'rb') as a_fd:
                    act_seq = pickle.load(a_fd)

                print ("Action test for", self.test_action_in_curr_state_from_seq(act_seq))

                if self.test_action_in_curr_state_from_seq(act_seq):
                    state_concepts_prob = self.get_state_concepts_from_classifier_with_prob(act_seq)
                    print ("Concepts", state_concepts_prob)
                    updated_prob = self.get_updated_probs(CURR_POSS_CONCEPTS, CURR_POSS_CONCEPTS_MAP, state_concepts_prob)

                    NEW_CURR_CONCEPTS = set()
                    # for conc in state_concepts_prob:
                    #     if conc in CURR_POSS_CONCEPTS:
                    #         NEW_CURR_CONCEPTS.add(conc)
                    NEW_CURR_CONCEPTS_MAP = {}
                    for conc in updated_prob:
                       if updated_prob[conc] > THRESHOLD_FOR_REMOVAL:
                           NEW_CURR_CONCEPTS.add(conc)
                           NEW_CURR_CONCEPTS_MAP[conc] = updated_prob[conc]
                    CURR_POSS_CONCEPTS = copy.deepcopy(NEW_CURR_CONCEPTS)
                    CURR_POSS_CONCEPTS_MAP = copy.deepcopy(NEW_CURR_CONCEPTS_MAP)

                print ("Remaining Concepts", CURR_POSS_CONCEPTS)
                #print ("Remaining Concepts distribution", CURR_POSS_CONCEPTS_MAP)
                if len(CURR_POSS_CONCEPTS) == 1: #and CURR_POSS_CONCEPTS_MAP[list(CURR_POSS_CONCEPTS)[0]] > 0.6:
                    print ("Found concept", CURR_POSS_CONCEPTS)
                    print ("Probability",CURR_POSS_CONCEPTS_MAP[list(CURR_POSS_CONCEPTS)[0]])
                    return list(CURR_POSS_CONCEPTS)[0]

                #if 'NOT_skull_on_left' not in CURR_POSS_CONCEPTS:
                #    exit(1)

                if sample_cnt >= SAMPLES_BUDGET:
                    print ("Concepts remaining",CURR_POSS_CONCEPTS_MAP)
                    print ("Concepts needed to execute action", list(CURR_POSS_CONCEPTS)[0])
                    return None

                elif len(CURR_POSS_CONCEPTS) == 0:
                    print ("Something wrong with", states_covered)
                    exit(1)
                #exit(1)
        print ("Concepts needed to execute action", list(CURR_POSS_CONCEPTS)[0])
