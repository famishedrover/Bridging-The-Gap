import os
import pickle

CONCEPT_DIR = "../DATA/CONCEPTS/MONTEZUMA/"
#prob_map = {'on_rope' : (1.0, 0.0), 'skull_on_right' : (0.75, 0.006172839506172839), 'on_middle_platform' : (1.0, 0.0), 'on_ladder3' : (1.0, 0.0), 'on_ladder2' : (1.0, 0.0), 'skull_on_left' : (0.8662790697674418, 0.005970149253731343) , 'die_on_left' : (1.0, 0.009345794392523364) , 'on_highest_platform' : (1.0, 0.001736111111111111), 'on_ground_and_alive' : (1.0, 0.0), 'on_ladder1' : (1.0, 0.0)}
#     {'on_rope' : 0.9988888888888889,'skull_on_right' : 0.75,'on_middle_platform' : 0.9988888888888889,'on_ladder3' : 1.0,'on_ladder2' : 1.0,'skull_on_left' : 0.89,'die_on_left' : 0.9885931558935361,'on_highest_platform' : 1.0,'on_ground_and_alive' : 1.0,'on_ladder1' : 1.0}
# prob_map_neg = {'on_rope' : 0.9988888888888889,'skull_on_right' : 0.75,'on_middle_platform' : 0.9988888888888889,'on_ladder3' : 1.0,'on_ladder2' : 1.0,'skull_on_left' : 0.89,'die_on_left' : 0.9885931558935361,'on_highest_platform' : 1.0,'on_ground_and_alive' : 1.0,'on_ladder1' : 1.0}

prob_map = {'on_ladder1': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'on_ladder2': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'on_ladder3': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'on_highest_platform': {'p_c_c': 1.0, 'p_nc_nc': 0.9982638888888888, 'p_nc_c': 0.0, 'p_c_nc': 0.001736111111111111},
            'on_rope': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'on_ground_and_alive': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'skull_on_right': {'p_c_c': 0.75, 'p_nc_nc': 0.9938271604938271, 'p_nc_c': 0.25, 'p_c_nc': 0.006172839506172839},
            'skull_on_left': {'p_c_c': 0.8662790697674418, 'p_nc_nc': 0.9940298507462687, 'p_nc_c': 0.13372093023255813, 'p_c_nc': 0.005970149253731343},
            'on_middle_platform': {'p_c_c': 1.0, 'p_nc_nc': 1.0, 'p_nc_c': 0.0, 'p_c_nc': 0.0},
            'die_on_left': {'p_c_c': 1.0, 'p_nc_nc': 0.9906542056074766, 'p_nc_c': 0.0, 'p_c_nc': 0.009345794392523364}}


class MontezumaConceptClass(object):
    def __init__(self):
        self.all_concepts = ['on_ladder1', 'on_ladder2', 'on_ladder3', 'on_highest_platform', 'on_rope', 'on_ground_and_alive', 'on_middle_platform', 'skull_on_right', 'skull_on_left', 'die_on_left']
        self.concept_models = {}
        self.load_model_file()

    def load_model_file(self):
        for concept in self.all_concepts:
            self.concept_models[concept] = pickle.load(open(os.path.join(os.path.join(CONCEPT_DIR, concept),'final_model.sav'), 'rb'))
                    

    def get_all_valid_concepts(self, current_state):
        valid_concept_map = {}
        for concept in self.all_concepts:
            #print ("Type for concept",concept, type(self.concept_models[concept]))
            # Note that right now we are only using the probabilities to calculate prob for negative prob
            # So if the observation is positive find the probabilites for the negation of the concept and vice versa
            if self.concept_models[concept].predict([current_state])[0] == 1 and self.concept_models[concept].predict_proba([current_state])[0][1] > 0.55:
                valid_concept_map[concept] = (1, prob_map[concept]['p_nc_nc'], prob_map[concept]['p_nc_c'])
            else:
                valid_concept_map[concept] = (0, prob_map[concept]['p_c_c'], prob_map[concept]['p_c_nc'])
        return valid_concept_map
