# Todo


import gym
import copy
import gym_sokoban_mod
import gym_sokoban_mod_gravity
from .constants import *
from itertools import combinations
from pydoc import locate

import numpy as np




class PriorSampler:
    def __init__(self, domain_name, foil_file, plan_cost, sampling_budget):
        self.sampling_budget = sampling_budget
        self.domain_name = domain_name
        self.explanation_prior = EXPLANATION_PRIOR
        self.executable_state_map = {}
        self.executable_state_cost_map = {}
        self.random_obj = np.random.RandomState()
        self.random_obj.seed(RAND_SEED)
        self.unique_actions = set()
        self.unique_action_costs = set()
        self.unique_concepts = []

        if self.domain_name == 'sokoban-gravity':
            # Create the sampler
            self.simulator_obj = SIMULATOR_INTERFACE_CLASS_MAP[self.domain_name]()
            self.sampler_interface_obj = SAMPLER_INTERFACE_CLASS_MAP[self.domain_name]()
            # Make the ConceptClassifierClass obj
            self.concept_obj = CONCEPT_CLASS_MAP[self.domain_name]()
            self.env = gym.make('Sokoban-gravity-mod-v0')
            self.all_concepts = CONCEPT_SET_FOR_GRAVITY
            self.observation_model = OBSERVATION_MODEL_GRAVITY
            self.executable_state_concept_prior = CONCEPT_PRIOR_FOR_GRAVITY
            self.executable_state_action_val_prior = ACTION_PRIOR_FOR_GRAVITY

        elif self.domain_name == 'sokoban-flip':
            # Create the sampler
            self.simulator_obj = SIMULATOR_INTERFACE_CLASS_MAP[self.domain_name]()
            self.sampler_interface_obj = SAMPLER_INTERFACE_CLASS_MAP[self.domain_name]()
            # Make the ConceptClassifierClass obj
            self.concept_obj = CONCEPT_CLASS_MAP[self.domain_name]()
            self.env = gym.make('Sokoban-mod-v0')
            self.all_concepts = CONCEPT_SET_FOR_FLIP
            self.observation_model = OBSERVATION_MODEL_FLIP
            self.executable_state_action_val_prior = {}
            self.executable_state_concept_prior = {}

        with open(foil_file) as f_fd:
             
            self.foil = []
            self.foil_cost_list = []
            foil_lines = [i.strip() for i in f_fd.readlines()]
            for fl in foil_lines:
                 self.foil.append(int(fl.split(':')[0]))
                 self.foil_cost_list.append(int(fl.split(':')[1]))

        # Get foil concept_list
        self.foil_states = self.get_foil_states()
        self.foil_cost = self.get_foil_cost()
        # for st in self.foil_states:
        #    print (st)
        # exit(0)
        self.plan_cost = plan_cost

        # TODO: Make sure to run a test here to double check its in fact better
        if self.foil_cost <= self.plan_cost:
            print ("Foil actually costs less, foils_cost",self.foil_cost,"plan_cost",self.plan_cost)
            exit(1)

    def get_foil_cost(self):
        curr_cost = 0
        for i in range(len(self.foil)):
            curr_cost += self.simulator_obj.get_action_cost(self.foil[:i], self.foil[i])
        return curr_cost

    def get_foil_states(self):
        state_obs = self.env.reset()
        foil_states = []
        foil_states.append(self.concept_obj.get_all_concepts_for_state(state_obs))
        # Turn into concepts
        for act in self.foil:
            state_obs, _, _, _ = self.env.step(act)
            foil_states.append(self.concept_obj.get_all_concepts_for_state(state_obs))
            # Turn into concepts
        return foil_states


    #def sampler_for_concept_set(self, conc_set):
    #    starting_concept = conc_set.pop()
    #    state_set = self.sampler_interface_obj.get_states_for_concept(starting_concept)
    #    for conc in conc_set:
    #        state_set &= self.sampler_interface_obj.get_states_for_concept(conc)
    #    return state_set

    def get_keys_for_concept_set(self, conc_set):
        if len(conc_set) == 0:
            return ''
        return "_".join(sorted(list(conc_set)))

    def create_state_execution_map(self, state_set, act):
        min_cost = float('inf')
        sample_cnt = 0
        conc_set_map = {}
        conc_set_map_cnt = {}
       
 
        for state in state_set:
            state_seq = self.sampler_interface_obj.get_state_seq(state)
            sample_cnt += 1
            if self.simulator_obj.test_action(state_seq, act):
                print ("Testing state",state, "min cost", min_cost)
                if act not in self.executable_state_map:
                    self.executable_state_map[act] = set()
                if state not in self.executable_state_cost_map:
                    self.executable_state_cost_map[state] = {}
                self.executable_state_map[act].add(state)

                curr_cost = self.simulator_obj.get_action_cost(state_seq, act)
                self.unique_action_costs.add(curr_cost)
                self.executable_state_cost_map[state][act] = curr_cost

            if sample_cnt >= self.sampling_budget:
                return conc_set_map, conc_set_map_cnt
        return conc_set_map, conc_set_map_cnt

    def calculate_act_priors(self, act, val):
            if act in self.executable_state_action_val_prior and val in self.executable_state_action_val_prior[act]:
                #assert self.executable_state_action_val_prior[act][val] !=0, "For act "+str(act) + " prior is zero"
                return self.executable_state_action_val_prior[act][val]
            else:
                state_list = list(self.executable_state_map[act])
                self.random_obj.shuffle(state_list)
                sampled_state = state_list[:min(len(state_list), SAMPLING_PRIOR_BUDGET)]
                val_cnt = 0
                for st in sampled_state:
                    if self.executable_state_cost_map[st][act] >= val:
                        val_cnt += 1
                if act not in self.executable_state_action_val_prior:
                    self.executable_state_action_val_prior[act] = {}
    
                self.executable_state_action_val_prior[act][val] = float(val_cnt)/len(sampled_state)
                #assert self.executable_state_action_val_prior[act][val] !=0, "For act "+str(act) + " val_cnt " + str(val_cnt) + " Sampled_state count"+len(sampled_state)
                return self.executable_state_action_val_prior[act][val]


    def calculate_concept_prior_for_executable_state(self, act, conc):
        conc_key = self.get_keys_for_concept_set(conc)
        if act in self.executable_state_concept_prior and conc_key in self.executable_state_concept_prior[act]:
            return self.executable_state_concept_prior[act][conc_key]
    
        else:
            state_list = list(self.executable_state_map[act])
            self.random_obj.shuffle(state_list)
            sampled_state = state_list[:min(len(state_list), SAMPLING_PRIOR_BUDGET)]
            conc_cnt = 0
            for st in sampled_state:
                pos_concept_set = self.sampler_interface_obj.get_concepts_for_state(st)
                full_concept_set = pos_concept_set | set([NEGATION_PREFIX + conc
                                                          for conc in (self.all_concepts - pos_concept_set)])
    
                if conc <= full_concept_set:
                    conc_cnt += 1
            if act not in self.executable_state_concept_prior:
                self.executable_state_concept_prior[act] = {}
            self.executable_state_concept_prior[act][conc_key] = float(conc_cnt) / len(sampled_state)
            #assert  self.executable_state_concept_prior[act][conc_key] != 0, " For concept "+ str(conc)+":"+str(act) +"--"+str(sampled_state) +"--"+str(full_concept_set)
            return self.executable_state_concept_prior[act][conc_key]


    def calculate_denominator(self, concept_set, act, val, curr_prior_on_cost):
        P_Ob_cost_given_cost_conc = 1
        P_Ob_cost_given_cost_not_conc = self.calculate_act_priors(act, val)
        P_Ob_cost_given_not_cost_conc = self.calculate_act_priors(act, val)
        P_Ob_cost_given_not_cost_not_conc = self.calculate_act_priors(act, val)

        P_Ob_conc_given_conc = 1
        for concept in concept_set:
            P_Ob_conc_given_conc *= self.observation_model[concept][OB_CONC][CONC]


        P_Ob_conc_given_not_conc = 1
        for concept in concept_set:
            P_Ob_conc_given_not_conc *= self.observation_model[concept][OB_CONC][NOT_CONC]

        P_conc = self.calculate_concept_prior_for_executable_state(act, concept_set)
        P_cost_fact = curr_prior_on_cost
        #print ("For act "+str(act))
        #print ("P_Ob_cost_given_cost_not_conc"+str(P_Ob_cost_given_cost_not_conc))
        #print ("P_conc "+str(P_conc))
        #print ("P_cost_fact "+str(curr_prior_on_cost))
        return (P_Ob_cost_given_cost_conc * P_Ob_conc_given_conc * P_cost_fact * P_conc)+\
               (P_Ob_cost_given_not_cost_conc *  P_Ob_conc_given_conc * (1 - P_cost_fact) * P_conc)+\
               (P_Ob_cost_given_cost_not_conc * P_Ob_conc_given_not_conc * P_cost_fact * (1 - P_conc))+\
               (P_Ob_cost_given_not_cost_not_conc * P_Ob_conc_given_not_conc * (1 - P_cost_fact) * (1 - P_conc))

    def calculate_numerator(self, concept_set, act, val, curr_prior_on_cost):
        P_Ob_cost_given_cost_conc = 1
        P_Ob_cost_given_cost_not_conc = self.calculate_act_priors(act, val)

        P_Ob_conc_given_conc = 1
        for concept in concept_set:
            P_Ob_conc_given_conc *= self.observation_model[concept][OB_CONC][CONC]

        P_Ob_conc_given_not_conc = 1
        for concept in concept_set:
            P_Ob_conc_given_not_conc *= self.observation_model[concept][OB_CONC][NOT_CONC]

        P_conc = self.calculate_concept_prior_for_executable_state(act, concept_set)
        P_cost_fact = curr_prior_on_cost

        return (P_Ob_cost_given_cost_conc * P_Ob_conc_given_conc * P_cost_fact * P_conc)+\
               (P_Ob_cost_given_cost_not_conc * P_Ob_conc_given_not_conc * P_cost_fact * (1 - P_conc))

    def calculate_the_confidence_of_explanation(self, concept, act, val, count):
        if concept == set(['']) or concept == set():
            return self.calculate_act_priors(act, val)

        curr_prob = self.explanation_prior

        for i in range(count):
            posterior = self.calculate_numerator(concept, act, val, curr_prob)/self.calculate_denominator(concept, act, val, curr_prob)
            curr_prob = posterior

        return curr_prob

    def find_all_proper_subsets(self, concept_set):
        subset_list = []
        for i in range(len(concept_set)):
            for comb in combinations(concept_set, i):
                subset_list.append(set(comb))
        return subset_list

    def find_min_subset_with_same_val(self, concept_set, act, val, val_maps):
        ordered_subsets = self.find_all_proper_subsets(concept_set)
        for subs in ordered_subsets:
            for indiv_map in val_maps:
                conc_map, conc_count = indiv_map[act]
                subs_key = self.get_keys_for_concept_set(subs)
                if subs_key in conc_map and conc_map[subs_key]>=val:
                    return subs
        return concept_set



    #def find_min_cost_for_conc_set_and_act(self, conc_set, act):
    #    state_set = self.sampler_for_concept_set(conc_set)
    #    print ("State set collected...")
    #    return self.find_min_cost_for_state_set(state_set, act)

    def create_priors(self, sampling_budget):
        self.sampling_budget = sampling_budget
        # For now ignoring empty concept set
        curr_concept_size = 1
        prev_memoized_list = []
        #while curr_concept_size < CONC_MAX:
        print ("Testing concept size", curr_concept_size)
        # check if the current concept set leads to a max
        plan_total = 0
        all_concepts_set = self.all_concepts | set([NEGATION_PREFIX + conc for conc in self.all_concepts])
        state_list = self.sampler_interface_obj.get_all_states()
        #print ("state",state_list)
        self.unique_actions = set(self.foil) 
        for foil_act in self.unique_actions:
            self.create_state_execution_map(state_list, foil_act)
        
        #print (len(self.executable_state_cost_map))
        #print (len(self.executable_state_map))
        for curr_concept_size in range(1,CONC_MAX):
            full_conc_set_list = [set(i) for i in combinations(all_concepts_set, curr_concept_size)]
            for conc in full_conc_set_list:
                if conc not in self.unique_concepts:
                    self.unique_concepts.append(conc)
            for act in self.unique_actions:
                for val in self.unique_action_costs:
                    self.calculate_act_priors(act,val)
                for conc in self.unique_concepts: 
                    self.calculate_concept_prior_for_executable_state(act,conc)

        #print ("self.executable_state_action_val_prior",self.executable_state_action_val_prior)

