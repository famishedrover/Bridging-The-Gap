import os

# Required classes
from .simulator_class.SokobanFlipSimulator import SokobanFlipSimulator
from .sampler_interface.SokobanSampler import SokobanFlipSampler
from .concept_class.SokobanFlip import SokobanFlipConceptClass

from .simulator_class.SokobanGravity import SokobanGravity
from .sampler_interface.SokobanSampler import SokobanGravitySampler
from .concept_class.SokobanGravity import SokobanGravityConceptClass

CONC_MAX = 10
FULL_SAMPLE_BUDGET = 750

SAMPLE_BUDGET = 10

CONCEPT_CLASS_MAP = {'sokoban-gravity': SokobanGravityConceptClass,
                     'sokoban-flip' : SokobanFlipConceptClass}
SAMPLER_INTERFACE_CLASS_MAP = {'sokoban-gravity': SokobanGravitySampler,
                               'sokoban-flip': SokobanFlipSampler}
SIMULATOR_INTERFACE_CLASS_MAP = {'sokoban-gravity': SokobanGravity,
                                 'sokoban-flip': SokobanFlipSimulator}
OBSERVATION_MODEL_GRAVITY = {'concept_blank_cell_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.1}}, 'NOT_concept_blank_cell_below': {'Ob_conc': {'conc': 0.9, 'not_conc': 0.0}}, 'concept_blank_cell_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.03333333333333333}}, 'NOT_concept_blank_cell_on_left': {'Ob_conc': {'conc': 0.9666666666666667, 'not_conc': 0.0}}, 'concept_box_below': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}}, 'NOT_concept_box_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}}, 'concept_box_on_left': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}}, 'NOT_concept_box_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}}, 'concept_box_on_right': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}}, 'NOT_concept_box_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}}, 'concept_box_on_top': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}}, 'NOT_concept_box_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}}, 'concept_no_pink_cell_below_m': {'Ob_conc': {'conc': 0.9940828402366864, 'not_conc': 0.0}}, 'NOT_concept_no_pink_cell_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.005917159763313609}}, 'concept_no_pink_cell_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_no_pink_cell_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_no_wall_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_no_wall_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_no_wall_on_left_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_no_wall_on_left_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_no_wall_on_right_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_no_wall_on_right_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_no_wall_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_no_wall_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_on_pink_cell': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_on_pink_cell': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_pink_cell_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_pink_cell_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_pink_cell_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_pink_cell_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_pink_cell_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.009302325581395349}}, 'NOT_concept_pink_cell_on_right': {'Ob_conc': {'conc': 0.9906976744186047, 'not_conc': 0.0}}, 'concept_pink_cell_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004878048780487805}}, 'NOT_concept_pink_cell_on_top': {'Ob_conc': {'conc': 0.9951219512195122, 'not_conc': 0.0}}, 'concept_target_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_target_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_target_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004545454545454545}}, 'NOT_concept_target_on_top': {'Ob_conc': {'conc': 0.9954545454545455, 'not_conc': 0.0}}, 'concept_wall_above_box': {'Ob_conc': {'conc': 0.9, 'not_conc': 0.0}}, 'NOT_concept_wall_above_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.1}}, 'concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_below_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_below_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_down_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_down_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_on_left_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_on_left_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_on_right_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_on_right_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_top_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_top_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_top_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_top_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_up_down_right': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}}, 'NOT_concept_wall_up_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}}}

# OBSERVATION_MODEL_GRAVITY = {'concept_blank_cell_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.13157894736842105}},
#                              'NOT_concept_blank_cell_below': {'Ob_conc': {'conc': 0.868421052631579, 'not_conc': 0.0}},
#                              'concept_blank_cell_on_left': {'Ob_conc': {'conc': 0.9929078014184397, 'not_conc': 0.03488372093023256}},
#                              'NOT_concept_blank_cell_on_left': {'Ob_conc': {'conc': 0.9651162790697675, 'not_conc': 0.0070921985815602835}},
#                              'concept_box_below': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                              'NOT_concept_box_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                              'concept_box_on_left': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                              'NOT_concept_box_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                              'concept_box_on_right': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                              'NOT_concept_box_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                              'concept_box_on_top': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                              'NOT_concept_box_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                              'concept_no_pink_cell_below_m': {'Ob_conc': {'conc': 0.9942528735632183, 'not_conc': 0.0}},
#                              'NOT_concept_no_pink_cell_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.005747126436781609}},
#                              'concept_no_pink_cell_on_top_m': {'Ob_conc': {'conc': 0.9943181818181818, 'not_conc': 0.0}},
#                              'NOT_concept_no_pink_cell_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.005681818181818182}},
#                              'concept_no_wall_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_no_wall_below_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_no_wall_on_left_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_no_wall_on_left_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_no_wall_on_right_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_no_wall_on_right_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_no_wall_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_no_wall_on_top_m': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_on_pink_cell': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_on_pink_cell': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_pink_cell_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004830917874396135}},
#                              'NOT_concept_pink_cell_below': {'Ob_conc': {'conc': 0.9951690821256038, 'not_conc': 0.0}},
#                              'concept_pink_cell_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004830917874396135}},
#                              'NOT_concept_pink_cell_on_left': {'Ob_conc': {'conc': 0.9951690821256038, 'not_conc': 0.0}},
#                              'concept_pink_cell_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_pink_cell_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_pink_cell_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004878048780487805}},
#                              'NOT_concept_pink_cell_on_top': {'Ob_conc': {'conc': 0.9951219512195122, 'not_conc': 0.0}},
#                              'concept_target_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_target_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_target_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.004545454545454545}},
#                              'NOT_concept_target_on_top': {'Ob_conc': {'conc': 0.9954545454545455, 'not_conc': 0.0}},
#                              'concept_wall_above_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_above_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_below_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_below_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_down_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_down_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_on_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_on_left_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_on_left_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_on_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_on_right_of_box': {'Ob_conc': {'conc': 0.9791666666666666, 'not_conc': 0.0}},
#                              'NOT_concept_wall_on_right_of_box': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.020833333333333332}},
#                              'concept_wall_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_on_top': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_top_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_top_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_top_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_top_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'concept_wall_up_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                              'NOT_concept_wall_up_down_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}}

OBSERVATION_MODEL_FLIP = {'concept_above_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_above_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_box_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_box_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_box_right': {'Ob_conc': {'conc': 0.8571428571428571, 'not_conc': 0.0}}, 'NOT_concept_box_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.14285714285714285}}, 'concept_empty_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_empty_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_empty_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_empty_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_empty_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0707070707070707}}, 'NOT_concept_empty_left': {'Ob_conc': {'conc': 0.9292929292929293, 'not_conc': 0.0}}, 'concept_empty_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.02586206896551724}}, 'NOT_concept_empty_right': {'Ob_conc': {'conc': 0.9741379310344828, 'not_conc': 0.0}}, 'concept_left_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_left_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_switch_on': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_switch_on': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_target_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0035460992907801418}}, 'NOT_concept_target_above': {'Ob_conc': {'conc': 0.9964539007092199, 'not_conc': 0.0}}, 'concept_target_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_target_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_target_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_target_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_target_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_target_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_left_below_ofbox': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_left_below_ofbox': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'concept_wall_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}, 'NOT_concept_wall_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}}

# OBSERVATION_MODEL_FLIP = {'concept_above_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_above_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_box_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_box_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_box_below': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                           'NOT_concept_box_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                           'concept_box_left': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                           'NOT_concept_box_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                           'concept_box_right': {'Ob_conc': {'conc': 0.0, 'not_conc': 0.0}},
#                           'NOT_concept_box_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 1.0}},
#                           'concept_empty_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.037037037037037035}},
#                           'NOT_concept_empty_above': {'Ob_conc': {'conc': 0.9629629629629629, 'not_conc': 0.0}},
#                           'concept_empty_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_empty_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_empty_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_empty_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_empty_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.008333333333333333}},
#                           'NOT_concept_empty_right': {'Ob_conc': {'conc': 0.9916666666666667, 'not_conc': 0.0}},
#                           'concept_left_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_left_switch': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_switch_on': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_switch_on': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_target_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0034965034965034965}},
#                           'NOT_concept_target_above': {'Ob_conc': {'conc': 0.9965034965034965, 'not_conc': 0.0}},
#                           'concept_target_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_target_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_target_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_target_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_target_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_target_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_wall_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_wall_above': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_wall_below': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_wall_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_wall_left': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_wall_left_below_ofbox': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_wall_left_below_ofbox': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'concept_wall_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}},
#                           'NOT_concept_wall_right': {'Ob_conc': {'conc': 1.0, 'not_conc': 0.0}}}


NEGATION_PREFIX = "NOT_"

CONCEPT_SET_FOR_FLIP = set(['concept_above_switch','concept_box_above','concept_box_below','concept_box_left',
                            'concept_box_right','concept_empty_above','concept_empty_below','concept_empty_left',
                            'concept_empty_right','concept_left_switch','concept_switch_on','concept_target_above',
                            'concept_target_below','concept_target_left','concept_target_right','concept_wall_above',
                            'concept_wall_below','concept_wall_left_below_ofbox','concept_wall_left','concept_wall_right'])


CONCEPT_SET_FOR_GRAVITY = set(['concept_blank_cell_below','concept_blank_cell_on_left','concept_box_below',
                                     'concept_box_on_left','concept_box_on_right','concept_box_on_top',
                                     'concept_no_pink_cell_below_m','concept_no_pink_cell_on_top_m',
                                     'concept_no_wall_below_m','concept_no_wall_on_left_m',
                                     'concept_no_wall_on_right_m','concept_no_wall_on_top_m',
                                     'concept_on_pink_cell','concept_pink_cell_below','concept_pink_cell_on_left',
                                     'concept_pink_cell_on_right','concept_pink_cell_on_top','concept_target_on_right',
                                     'concept_target_on_top','concept_wall_above_box','concept_wall_below_box',
                                     'concept_wall_below','concept_wall_down_left','concept_wall_down_right',
                                     'concept_wall_on_left_of_box','concept_wall_on_left','concept_wall_on_right_of_box',
                                     'concept_wall_on_right','concept_wall_on_top','concept_wall_top_left',
                                     'concept_wall_top_right','concept_wall_up_down_right'])

CONCEPT_PRIOR_FOR_GRAVITY = {}
CONCEPT_PRIOR_FOR_FLIP = {}
EXPLANATION_PRIOR = 0.5
SAMPLING_PRIOR_BUDGET = 100

# Random variable list
CONC = 'conc'
OB_CONC = 'Ob_conc'
NOT_CONC = 'not_conc'
NOT_OB_CONC = 'not_Ob_conc'
COST_FACT = 'costfact'
OBS_COST = 'Ob_costfact'

RAND_SEED = 5
