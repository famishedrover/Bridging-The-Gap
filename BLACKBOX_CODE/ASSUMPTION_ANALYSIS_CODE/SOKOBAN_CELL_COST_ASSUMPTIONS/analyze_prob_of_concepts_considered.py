ACTION_LOOKUP = {
0: "no operation",
1: "push up",
2: "push down",
3: "push left",
4: "push right",
5: "move up",
6: "move down",
7: "move left",
8: "move right",
}


import yaml
with open('concept_cnt_switch_for_icml_cost_10_analysis.yaml') as c_fd:
    concept_dict = yaml.load(c_fd)

concept_set = set(['concept_blank_cell_below', 'concept_blank_cell_on_left', 'concept_box_below', 'concept_box_on_left', 'concept_box_on_right', 'concept_box_on_top', 'concept_no_pink_cell_below_m', 'concept_no_pink_cell_on_top_m', 'concept_no_wall_below_m', 'concept_no_wall_on_left_m', 'concept_no_wall_on_right_m', 'concept_no_wall_on_top_m', 'concept_on_pink_cell', 'concept_pink_cell_below', 'concept_pink_cell_on_left', 'concept_pink_cell_on_right', 'concept_pink_cell_on_top', 'concept_target_on_right', 'concept_target_on_top', 'concept_wall_above_box', 'concept_wall_below', 'concept_wall_below_box', 'concept_wall_down_left', 'concept_wall_down_right', 'concept_wall_on_left', 'concept_wall_on_left_of_box', 'concept_wall_on_right', 'concept_wall_on_right_of_box', 'concept_wall_on_top', 'concept_wall_top_left', 'concept_wall_top_right', 'concept_wall_up_down_right'])


#TODO: change for action costs

per_action_concept_ratio = []
for act_id in [1,2,3,4]: #range(len(concept_dict['concept_count_mark'])):
    conc_map = concept_dict['concept_count_mark'][act_id]
    curr_action_ratio = {}
    for conc in conc_map:
        if conc in concept_set:
            curr_action_ratio[conc] = float(conc_map[conc])/concept_dict['total_concept_count_mark'][act_id][conc]
    
    per_action_concept_ratio.append(curr_action_ratio)

per_action_ratio = []

for act_id in [1,2,3,4]:
    per_action_ratio.append(float(concept_dict['act_cost_count'][act_id])/concept_dict['action_count'][act_id])

act_id = 0
for conc_ratio in per_action_concept_ratio:
    #print ("Action id", act_id, ACTION_LOOKUP[act_id])
    max_conc = None
    max_diff = -1
    total_diff = 0
    for conc in conc_ratio:
        curr_diff = abs(per_action_ratio[act_id] - conc_ratio[conc])
        total_diff += curr_diff
        if curr_diff > max_diff:
            max_conc = conc
            max_diff = curr_diff
    #print ("Concept is", max_conc,"and the diff is",max_diff, "average is", total_diff/len(conc_ratio))
    print ("&",ACTION_LOOKUP[act_id+1],"&",max_conc.replace('_','\_'),"&", round(max_diff,4),"&", round(total_diff/len(conc_ratio),4),"\\\\")
    act_id += 1