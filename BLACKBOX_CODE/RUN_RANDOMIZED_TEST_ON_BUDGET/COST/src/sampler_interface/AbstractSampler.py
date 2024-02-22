class AbstractSampler:
    def __init__(self):
        pass

    def get_states_for_concept(self, concept):
        pass

    def get_states_for_concept_set(self, concept_set):
        state_set = set()
        first_time = True
        for concept in concept_set:
            conc_state_set = self.get_states_for_concept(concept)
            if first_time:
                state_set |= conc_state_set
                first_time = False
            else:
                state_set &= conc_state_set
        return state_set