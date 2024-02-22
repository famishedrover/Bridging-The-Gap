import torch

from CNNNetwork import Net

CONCEPT_TO_MODEL_MAP = {
    'concept_above_switch': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_above_switch.pth',
    'concept_box_above': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_box_above.pth',
    'concept_box_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_box_below.pth',
    'concept_box_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_box_left.pth',
    'concept_box_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_box_right.pth',
    'concept_empty_above': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_empty_above.pth',
    'concept_empty_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_empty_below.pth',
    'concept_empty_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_empty_left.pth',
    'concept_empty_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_empty_right.pth',
    'concept_left_switch': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_left_switch.pth',
    'concept_switch_on': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_switch_on.pth',
    'concept_target_above': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_target_above.pth',
    'concept_target_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_target_below.pth',
    'concept_target_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_target_left.pth',
    'concept_target_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_target_right.pth',
    'concept_wall_above': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_wall_above.pth',
    'concept_wall_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_wall_below.pth',
    'concept_wall_left_below_ofbox': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_wall_left_below_ofbox.pth',
    'concept_wall_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_wall_left.pth',
    'concept_wall_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/FLIP_MODELS/concept_wall_right.pth'}

CONCEPT_TO_MODEL_MAP_FOR_GRAVITY = {
'concept_blank_cell_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_blank_cell_below.pth',
'concept_blank_cell_on_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_blank_cell_on_left.pth',
'concept_box_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_box_below.pth',
'concept_box_on_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_box_on_left.pth',
'concept_box_on_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_box_on_right.pth',
'concept_box_on_top': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_box_on_top.pth',
'concept_no_pink_cell_below_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_pink_cell_below_m.pth',
'concept_no_pink_cell_on_top_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_pink_cell_on_top_m.pth',
'concept_no_wall_below_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_wall_below_m.pth',
'concept_no_wall_on_left_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_wall_on_left_m.pth',
'concept_no_wall_on_right_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_wall_on_right_m.pth',
'concept_no_wall_on_top_m': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_no_wall_on_top_m.pth',
'concept_on_pink_cell': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_on_pink_cell.pth',
'concept_pink_cell_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_pink_cell_below.pth',
'concept_pink_cell_on_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_pink_cell_on_left.pth',
'concept_pink_cell_on_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_pink_cell_on_right.pth',
'concept_pink_cell_on_top': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_pink_cell_on_top.pth',
'concept_target_on_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_target_on_right.pth',
'concept_target_on_top': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_target_on_top.pth',
'concept_wall_above_box': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_above_box.pth',
'concept_wall_below_box': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_below_box.pth',
'concept_wall_below': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_below.pth',
'concept_wall_down_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_down_left.pth',
'concept_wall_down_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_down_right.pth',
'concept_wall_on_left_of_box': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_on_left_of_box.pth',
'concept_wall_on_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_on_left.pth',
'concept_wall_on_right_of_box': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_on_right_of_box.pth',
'concept_wall_on_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_on_right.pth',
'concept_wall_on_top': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_on_top.pth',
'concept_wall_top_left': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_top_left.pth',
'concept_wall_top_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_top_right.pth',
'concept_wall_up_down_right': '/home/yochan/mycode/blackboxexp/COST_EXPLANATION/src/DATA/GRAVITY_MODELS/concept_wall_up_down_right.pth'}

def run_classifier(concept_name, state):
    #concept_name = 'concept_switch_on'
    #if concept_name in CONCEPT_TO_MODEL_MAP:
    print ("Concept",concept_name)
    net = Net()
    net.load_state_dict(torch.load(CONCEPT_TO_MODEL_MAP[concept_name]))
    net.eval()
    output = net(torch.tensor([state]).permute(0,3,1,2).float())
    _, predicted = torch.max(output.data, 1)
    output_arr = output.detach().numpy()[0]
    #print ("output", predicted[0])
    if predicted[0] != 0:
        return True
    else:
        return False
    #else:
    #    return -1

def run_classifier_gravity(concept_name, state):
    #concept_name = 'concept_switch_on'
    #if concept_name in CONCEPT_TO_MODEL_MAP:
    print ("Concept",concept_name)
    net = Net()
    net.load_state_dict(torch.load(CONCEPT_TO_MODEL_MAP_FOR_GRAVITY[concept_name]))
    net.eval()
    output = net(torch.tensor([state]).permute(0,3,1,2).float())
    _, predicted = torch.max(output.data, 1)
    output_arr = output.detach().numpy()[0]
    #print ("output", predicted[0])
    if predicted[0] != 0:
        return True
    else:
        return False
    #else:
    #    return -1
