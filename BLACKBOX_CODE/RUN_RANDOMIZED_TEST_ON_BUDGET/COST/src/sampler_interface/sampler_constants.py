import os
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)

DATA_DIR = os.path.join(SRC_DIR, 'DATA')

SOKOBAN_GRAVITY_DATA = os.path.join(DATA_DIR, 'GRAVITY_SAMPLES')

MODEL_DIR = os.path.join(DATA_DIR, 'MODELS')
SOKOBAN_FLIP_DATA = os.path.join(DATA_DIR, 'FLIP_SAMPLES')


CONCEPT_MAP_FILE_NAME_PREFIX = 'CONCEPT_MAP'


EMPTY_CONCEPTS = 'ALL'
SAMPLE_STATE_FILE_PREFIX = "state"
SAMPLE_STATE_SEQ_FILE_SUFFIX = "_seq.png"
SAMPLE_STATE_IMG_FILE_SUFFIX = "_img.png"

# Change to listing file names

CONCEPT_FILE_NAME_FOR_FLIP = set(['ALL','concept_above_switch','concept_box_above','concept_box_below','concept_box_left',
                                  'concept_box_right','concept_empty_above','concept_empty_below','concept_empty_left',
                                  'concept_empty_right','concept_left_switch','concept_switch_on','concept_target_above',
                                  'concept_target_below','concept_target_left','concept_target_right','concept_wall_above',
                                  'concept_wall_below','concept_wall_left_below_ofbox','concept_wall_left','concept_wall_right'])

CONCEPT_FILE_NAME_FOR_GRAVITY = set(['ALL','concept_blank_cell_below','concept_blank_cell_on_left','concept_box_below',
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