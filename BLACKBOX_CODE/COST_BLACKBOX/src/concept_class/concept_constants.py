import os
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)

DATA_DIR = os.path.join(SRC_DIR, 'DATA')

FLIP_MODELS_DIR = os.path.join(DATA_DIR, 'FLIP_MODELS')
GRAVITY_MODEL_DIR = os.path.join(DATA_DIR, 'GRAVITY_MODELS')

CONCEPT_TO_MODEL_MAP_FOR_FLIP = {
'concept_above_switch': FLIP_MODELS_DIR + '/concept_above_switch.pth',
#'concept_box_above': FLIP_MODELS_DIR + '/concept_box_above.pth',
#'concept_box_below': FLIP_MODELS_DIR + '/concept_box_below.pth',
'concept_box_left': FLIP_MODELS_DIR + '/concept_box_left.pth',
'concept_box_right': FLIP_MODELS_DIR + '/concept_box_right.pth',
'concept_empty_above': FLIP_MODELS_DIR + '/concept_empty_above.pth',
'concept_empty_below': FLIP_MODELS_DIR + '/concept_empty_below.pth',
'concept_empty_left': FLIP_MODELS_DIR + '/concept_empty_left.pth',
'concept_empty_right': FLIP_MODELS_DIR + '/concept_empty_right.pth',
'concept_left_switch': FLIP_MODELS_DIR + '/concept_left_switch.pth',
'concept_switch_on': FLIP_MODELS_DIR + '/concept_switch_on.pth',
'concept_target_above': FLIP_MODELS_DIR + '/concept_target_above.pth',
'concept_target_below': FLIP_MODELS_DIR + '/concept_target_below.pth',
'concept_target_left': FLIP_MODELS_DIR + '/concept_target_left.pth',
'concept_target_right': FLIP_MODELS_DIR + '/concept_target_right.pth',
'concept_wall_above': FLIP_MODELS_DIR + '/concept_wall_above.pth',
'concept_wall_below': FLIP_MODELS_DIR + '/concept_wall_below.pth',
'concept_wall_left_below_ofbox': FLIP_MODELS_DIR + '/concept_wall_left_below_ofbox.pth',
'concept_wall_left': FLIP_MODELS_DIR + '/concept_wall_left.pth',
'concept_wall_right': FLIP_MODELS_DIR + '/concept_wall_right.pth'}

CONCEPT_TO_MODEL_MAP_FOR_GRAVITY = {
'concept_blank_cell_below': GRAVITY_MODEL_DIR + '/concept_blank_cell_below.pth',
'concept_blank_cell_on_left': GRAVITY_MODEL_DIR + '/concept_blank_cell_on_left.pth',
'concept_box_below': GRAVITY_MODEL_DIR + '/concept_box_below.pth',
'concept_box_on_left': GRAVITY_MODEL_DIR + '/concept_box_on_left.pth',
'concept_box_on_right': GRAVITY_MODEL_DIR + '/concept_box_on_right.pth',
'concept_box_on_top': GRAVITY_MODEL_DIR + '/concept_box_on_top.pth',
'concept_no_pink_cell_below_m': GRAVITY_MODEL_DIR + '/concept_no_pink_cell_below_m.pth',
'concept_no_pink_cell_on_top_m': GRAVITY_MODEL_DIR + '/concept_no_pink_cell_on_top_m.pth',
'concept_no_wall_below_m': GRAVITY_MODEL_DIR + '/concept_no_wall_below_m.pth',
'concept_no_wall_on_left_m': GRAVITY_MODEL_DIR + '/concept_no_wall_on_left_m.pth',
'concept_no_wall_on_right_m': GRAVITY_MODEL_DIR + '/concept_no_wall_on_right_m.pth',
'concept_no_wall_on_top_m': GRAVITY_MODEL_DIR + '/concept_no_wall_on_top_m.pth',
'concept_on_pink_cell': GRAVITY_MODEL_DIR + '/concept_on_pink_cell.pth',
'concept_pink_cell_below': GRAVITY_MODEL_DIR + '/concept_pink_cell_below.pth',
'concept_pink_cell_on_left': GRAVITY_MODEL_DIR + '/concept_pink_cell_on_left.pth',
'concept_pink_cell_on_right': GRAVITY_MODEL_DIR + '/concept_pink_cell_on_right.pth',
'concept_pink_cell_on_top': GRAVITY_MODEL_DIR + '/concept_pink_cell_on_top.pth',
'concept_target_on_right': GRAVITY_MODEL_DIR + '/concept_target_on_right.pth',
'concept_target_on_top': GRAVITY_MODEL_DIR + '/concept_target_on_top.pth',
'concept_wall_above_box': GRAVITY_MODEL_DIR + '/concept_wall_above_box.pth',
'concept_wall_below': GRAVITY_MODEL_DIR + '/concept_wall_below.pth',
'concept_wall_below_box': GRAVITY_MODEL_DIR + '/concept_wall_below_box.pth',
'concept_wall_down_left': GRAVITY_MODEL_DIR + '/concept_wall_down_left.pth',
'concept_wall_down_right': GRAVITY_MODEL_DIR + '/concept_wall_down_right.pth',
'concept_wall_on_left': GRAVITY_MODEL_DIR + '/concept_wall_on_left.pth',
'concept_wall_on_left_of_box': GRAVITY_MODEL_DIR + '/concept_wall_on_left_of_box.pth',
'concept_wall_on_right': GRAVITY_MODEL_DIR + '/concept_wall_on_right.pth',
'concept_wall_on_right_of_box': GRAVITY_MODEL_DIR + '/concept_wall_on_right_of_box.pth',
'concept_wall_on_top': GRAVITY_MODEL_DIR + '/concept_wall_on_top.pth',
'concept_wall_top_left': GRAVITY_MODEL_DIR + '/concept_wall_top_left.pth',
'concept_wall_top_right': GRAVITY_MODEL_DIR + '/concept_wall_top_right.pth',
'concept_wall_up_down_right': GRAVITY_MODEL_DIR + '/concept_wall_up_down_right.pth'
}
