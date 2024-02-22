from .AbstractSampler import AbstractSampler
from .sampler_constants import *
import os

class SokobanGravitySampler(AbstractSampler):
    def __init__(self):
        self.concept_set = CONCEPT_FILE_NAME_FOR_GRAVITY
        self.concept_state_map = {}
        for conc in self.concept_set:
            concept_file_path = os.path.join(os.path.join(SOKOBAN_GRAVITY_DATA, CONCEPT_MAP_FILE_NAME_PREFIX), conc)
            if os.path.exists(concept_file_path):
                with open(concept_file_path) as p_fd:
                    self.concept_state_map[conc] = set([i.strip() for i in p_fd.readlines()])
            else:
                self.concept_state_map[conc] = set()

    def get_states_for_concept(self, concept):
        with open(os.path.join(os.path.join(SOKOBAN_GRAVITY_DATA, CONCEPT_MAP_FILE_NAME_PREFIX),concept)) as p_fd:
            state_list = [i.strip() for i in p_fd.readlines()]
        return set(state_list)

    def get_all_states(self):
        with open(os.path.join(os.path.join(SOKOBAN_GRAVITY_DATA, CONCEPT_MAP_FILE_NAME_PREFIX),EMPTY_CONCEPTS)) as p_fd:
            state_list = [i.strip() for i in p_fd.readlines()]
        return set(state_list)

    def get_state_seq(self, state_id):
        with open(os.path.join(SOKOBAN_GRAVITY_DATA,  SAMPLE_STATE_FILE_PREFIX+state_id+SAMPLE_STATE_SEQ_FILE_SUFFIX)) as p_fd:
            act_seq = [int(i) for i in p_fd.readlines()]
        return act_seq

    def get_concepts_for_state(self, state_id):
        concepts_supported = set()
        for conc in self.concept_state_map:
            if state_id in  self.concept_state_map[conc]:
                concepts_supported.add(conc)
        return concepts_supported



class SokobanFlipSampler(AbstractSampler):
    def __init__(self):
        self.concept_set = CONCEPT_FILE_NAME_FOR_FLIP
        self.concept_state_map = {}
        for conc in self.concept_set:
            concept_file_path = os.path.join(os.path.join(SOKOBAN_FLIP_DATA, CONCEPT_MAP_FILE_NAME_PREFIX), conc)
            if os.path.exists(concept_file_path):
                with open(concept_file_path) as p_fd:
                    self.concept_state_map[conc] = set([i.strip() for i in p_fd.readlines()])
            else:
                self.concept_state_map[conc] = set()

    def get_states_for_concept(self, concept):
        with open(os.path.join(os.path.join(SOKOBAN_FLIP_DATA, CONCEPT_MAP_FILE_NAME_PREFIX),concept)) as p_fd:
            state_list = [i.strip() for i in p_fd.readlines()]
        return set(state_list)

    def get_all_states(self):
        with open(os.path.join(os.path.join(SOKOBAN_FLIP_DATA, CONCEPT_MAP_FILE_NAME_PREFIX),EMPTY_CONCEPTS)) as p_fd:
            state_list = [i.strip() for i in p_fd.readlines()]
        return set(state_list)

    def get_state_seq(self, state_id):
        with open(os.path.join(SOKOBAN_FLIP_DATA,  SAMPLE_STATE_FILE_PREFIX+state_id+SAMPLE_STATE_SEQ_FILE_SUFFIX)) as p_fd:
            act_seq = [int(i) for i in p_fd.readlines()]
        return act_seq

    def get_concepts_for_state(self, state_id):
        concepts_supported = set()
        for conc in self.concept_state_map:
            if state_id in  self.concept_state_map[conc]:
                concepts_supported.add(conc)
        return concepts_supported

if __name__ == '__main__':
    samp = SokobanFlipSampler()
    print ("States",samp.get_states_for_concept('concept_switch_on'))
    print ("State seq", samp.get_state_seq('0'))
