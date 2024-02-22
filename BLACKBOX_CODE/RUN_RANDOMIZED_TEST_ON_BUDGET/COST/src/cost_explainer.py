# Todo


import gym
import copy
import gym_sokoban_mod
import gym_sokoban_mod_gravity
from .constants import *
from itertools import combinations
from pydoc import locate

import numpy as np




class CostExplanation:
    def __init__(self, domain_name, foil_file, plan_cost, sampling_budget):
        self.sampling_budget = sampling_budget
        self.domain_name = domain_name
        self.explanation_prior = EXPLANATION_PRIOR
        self.executable_state_map = {}
        self.executable_state_cost_map = {}
        self.random_obj = np.random.RandomState()
        self.random_obj.seed(RAND_SEED)
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
            self.executable_state_concept_prior = CONCEPT_PRIOR_FOR_FLIP
            self.executable_state_action_val_prior = ACTION_PRIOR_FOR_FLIP


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

    def find_min_cost_for_concept_state_set(self, state_set, act, conc_set_list, foil_cost, fstate):
        min_cost = float('inf')
        sample_cnt = 0
        conc_set_map = {}
        conc_set_map_cnt = {}
       
        for conc_set in conc_set_list:
            conc_set_key = self.get_keys_for_concept_set(conc_set)
            conc_set_map[conc_set_key] = foil_cost
            conc_set_map_cnt[conc_set_key] = 1
            if act not in self.executable_state_map:
                self.executable_state_map[act] = set()
            if fstate not in self.executable_state_cost_map:
                self.executable_state_cost_map[fstate] = {}
            self.executable_state_map[act].add(fstate)

            self.executable_state_cost_map[fstate][act] = foil_cost



 
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
                self.executable_state_cost_map[state][act] = curr_cost

                pos_concept_set = self.sampler_interface_obj.get_concepts_for_state(state)
                full_concept_set = pos_concept_set | set([NEGATION_PREFIX + conc
                                                          for conc in (self.all_concepts - pos_concept_set)])
                sample_cnt_not_met = False
                for conc_set in conc_set_list:
                    conc_set_key = self.get_keys_for_concept_set(conc_set)
                    #if conc_set_map_cnt.get(conc_set_key,0) < self.sampling_budget:
                    #sample_cnt_not_met = True
                    if conc_set <= full_concept_set:
                            #if 'concept_on_pink_cell' in conc_set:
                            #    print ("State:", state_seq, curr_cost)
                            #if conc_set_key not in conc_set_map:
                            #    conc_set_map[conc_set_key] = float('inf')
                            #    conc_set_map_cnt[conc_set_key] = 0
                            if conc_set_map[conc_set_key] >= curr_cost:
                                conc_set_map[conc_set_key] = curr_cost
                                conc_set_map_cnt[conc_set_key] += 1

                if curr_cost < min_cost:
                    min_cost = curr_cost
            if sample_cnt >= self.sampling_budget:
            #if not sample_cnt_not_met:
                conc_set_map[''] = min_cost
                conc_set_map_cnt[''] = sample_cnt
                return conc_set_map, conc_set_map_cnt
        conc_set_map[''] = min_cost
        conc_set_map_cnt[''] = sample_cnt
        return conc_set_map, conc_set_map_cnt

    def calculate_act_priors(self, act, val):
        return self.executable_state_action_val_prior[act][val]

    def calculate_concept_prior_for_executable_state(self, act, conc):
        conc_key = self.get_keys_for_concept_set(conc)
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

    def find_concept_set_prioritize_number_of_concepts(self, sampling_budget):
        #target_concept = 'NOT_concept_switch_on'
        target_concept = 'concept_on_pink_cell'

        target_prob = -1
        target_value = -1
        self.sampling_budget = sampling_budget
        # For now ignoring empty concept set
        curr_concept_size = 1
        prev_memoized_list = []
        while curr_concept_size < CONC_MAX:
            print ("Testing concept size", curr_concept_size)
            # check if the current concept set leads to a max
            plan_total = 0
            curr_max_conc = []
            memoized_list = {}
            all_concepts_set = self.all_concepts | set([NEGATION_PREFIX + conc for conc in self.all_concepts])

            for step_id in range(len(self.foil)):
                print ("state size", len(self.executable_state_cost_map))
                foil_state = self.foil_states[step_id]
                foil_act = self.foil[step_id]
                foil_cost = self.foil_cost_list[step_id]
                #foil_state_key = '_'.join(sorted(list(foil_state))) + '_'+ str(foil_act)
                full_state = foil_state | set([NEGATION_PREFIX + conc for conc in (self.all_concepts - foil_state)])
                foil_state_name = "f_"+str(step_id) 

                #print ("Searching for step id", step_id, full_state)
                self.sampler_interface_obj.add_state(foil_state_name, full_state)
                if foil_act in memoized_list:
                    conc_set_map, conc_set_cnt = memoized_list[foil_act]
                else:
                    conc_set_map = {}
                    conc_set_cnt = {}

                full_conc_set_list = [set(i) for i in combinations(full_state, curr_concept_size)]
                #print (full_conc_set_list)
                #print ("Concepts for 365", self.sampler_interface_obj.get_concepts_for_state('365'))
                #exit(1)
                missing_conc_set_list = []
                for conc_set in full_conc_set_list:
                    conc_set_key = self.get_keys_for_concept_set(conc_set)
                    if conc_set_key not in conc_set_map:
                        missing_conc_set_list.append(conc_set)

                updated_conc_set_map, updated_conc_set_cnt = self.find_min_cost_for_concept_state_set(
                        self.sampler_interface_obj.get_all_states(), foil_act, missing_conc_set_list, foil_cost, foil_state_name)
                for key in updated_conc_set_map:
                    if key not in conc_set_map:
                        conc_set_map[key] = updated_conc_set_map[key]
                        conc_set_cnt[key] = updated_conc_set_cnt[key]

                memoized_list[foil_act] = (conc_set_map, conc_set_cnt)
                    #print (conc_set_map)
                    #exit(0)
                state_conc_set_list = [set(i) for i in combinations(full_state, curr_concept_size)]
                max_set_list = None
                max_val = float('-inf')
        
                for conc_set in state_conc_set_list:
                    conc_set_key = self.get_keys_for_concept_set(conc_set)
                    curr_val = conc_set_map.get(conc_set_key,float('-inf'))
                    # Todo: Use sample cnt for explanations
                    if curr_val > max_val:
                        max_set_list = [conc_set]
                        max_val = curr_val
                    elif curr_val == max_val:
                        max_set_list.append(conc_set)


                print ("###############", max_set_list)
              
                print ("###############", max_val)

                for conc_set in max_set_list:
                    if target_concept in conc_set:
                        target_value = max_val
                        #target_prob = self.calculate_the_confidence_of_explanation(curr_conc_set, foil_act,
                        #                                                         max_val, conc_set_cnt[
                        #                                                             self.get_keys_for_concept_set(
                        #                                                                 curr_conc_set)])
                        print ("Count...",conc_set_cnt[target_concept])
                # find the concept with max prob

                best_conc_set = max_set_list.pop()
                best_conc_set_prob = self.calculate_the_confidence_of_explanation(best_conc_set, foil_act,
                                                                                       max_val, conc_set_cnt[
                                                                                      self.get_keys_for_concept_set(
                                                                                          best_conc_set)])
                if target_concept in best_conc_set:
                    if best_conc_set_prob > target_prob:
                        target_prob = best_conc_set_prob
                for curr_conc_set in max_set_list:
                    conc_set_prob = self.calculate_the_confidence_of_explanation(curr_conc_set, foil_act,
                                                                                 max_val, conc_set_cnt[
                                                                                     self.get_keys_for_concept_set(
                                                                                         curr_conc_set)])
                    if conc_set_prob > best_conc_set_prob:
                        best_conc_set = curr_conc_set

                    if target_concept in curr_conc_set:
                        if best_conc_set_prob > target_prob:
                            target_prob = best_conc_set_prob



                # check if any subset would do provide the same value
                #min_sub_set = self.find_min_subset_with_same_val(best_conc_set, foil_act, max_val, prev_memoized_list + [memoized_list])
                # if min set is not the same the original set recalculate the prob
                #if min_sub_set != best_conc_set:
                #    cnt = 0
                #    min_sub_set_key = self.get_keys_for_concept_set(curr_conc_set)
                #    for prev_conc_dict in prev_memoized_list + [memoized_list]:
                #        prev_conc_set, prev_conc_count = prev_conc_dict[foil_act]
                #        cnt = prev_conc_count[min_sub_set_key]
                #    best_conc_set_prob = self.calculate_the_confidence_of_explanation(min_sub_set, foil_act, max_val, cnt)

                curr_max_conc.append((best_conc_set, max_val, best_conc_set_prob))
                print ("Cost of action", best_conc_set, max_val, best_conc_set_prob)
                #print (conc_set_map, conc_set_cnt)
                plan_total += max_val
            print ("Current plan total",plan_total)
            #exit(1)
            if plan_total > self.plan_cost:
                return curr_max_conc, target_prob
            curr_concept_size += 1
            prev_memoized_list.append(copy.deepcopy(memoized_list))



        print ("Error!! Couldn't find an explanation for the given concept size limit, Try increasing CONC_MAX")
        return []




