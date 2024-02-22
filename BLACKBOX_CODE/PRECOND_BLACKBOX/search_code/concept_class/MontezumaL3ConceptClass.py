import os
import pickle

CONCEPT_DIR = "../DATA/CONCEPTS/MONTEZUMAL4/"

prob_map = {'onLadderTop': {'p_nc_c': 0.00645, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 0.99355},
            'inAir': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
            'isClearUpCrab': {'p_nc_c': 0.00968, 'p_nc_nc': 0.99661, 'p_c_nc': 0.00339, 'p_c_c': 0.99032},
            'crabLiesToRight': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
            'isClearDownCrab': {'p_nc_c': 0.00645, 'p_nc_nc': 0.99322, 'p_c_nc': 0.00678, 'p_c_c': 0.99354},
            'onLadderBottom': {'p_nc_c': 0.0, 'p_nc_nc': 0.99492, 'p_c_nc': 0.00508, 'p_c_c': 1.0},
            'crabLiesToLeft': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
            'onLadder': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
            'onLeftPassage': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0},
            'onRightPassage': {'p_nc_c': 0.0, 'p_nc_nc': 1.0, 'p_c_nc': 0.0, 'p_c_c': 1.0}}


class MontezumaL3ConceptClass(object):
    def __init__(self):
        self.all_concepts =  ["onLadder","inAir",
                             "isClearDownCrab","isClearUpCrab",
                             "crabLiesToLeft", "crabLiesToRight",
                             "onLadderBottom",
                             "onLadderTop","onLeftPassage","onRightPassage"]

        self.concept_models = {}
        self.load_model_file()

    def load_model_file(self):
        for concept in self.all_concepts:
            self.concept_models[concept] = pickle.load(open(os.path.join(os.path.join(CONCEPT_DIR, concept),
                                                                         'final_model.sav'), 'rb'))


    def get_all_valid_concepts(self, current_state):
        valid_concept_map = {}
        for concept in self.all_concepts:
            #print ("Type for concept",concept, type(self.concept_models[concept]))
            #prob = prob_map[concept]
            if self.concept_models[concept].predict([current_state])[0] == 1 and self.concept_models[concept].predict_proba([current_state])[0][1]> 0.5:
                valid_concept_map[concept] = (1, prob_map[concept]['p_nc_nc'], prob_map[concept]['p_nc_c'])
                #valid_concept_map[concept] = (1, self.concept_models[concept].predict_proba([current_state])[0][1])
                #valid_concept_map[concept] = (1, prob)
            else:
                #valid_concept_map[concept] = (0, self.concept_models[concept].predict_proba([current_state])[0][0])
                valid_concept_map[concept] = (0, prob_map[concept]['p_c_c'], prob_map[concept]['p_c_nc'])
                #valid_concept_map[concept] = (0, prob)
        return valid_concept_map
