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
with open('concept_cnt_switch_for_icml_prec_analysis.yaml') as c_fd:
    concept_dict = yaml.load(c_fd)

concept_set = set(['concept_above_switch', 'concept_box_left', 'concept_box_right', 'concept_empty_above', 'concept_empty_below', 'concept_empty_left', 'concept_empty_right', 'concept_left_switch', 'concept_switch_on', 'concept_target_above', 'concept_target_below', 'concept_target_left', 'concept_target_right', 'concept_wall_above', 'concept_wall_below', 'concept_wall_left_below_ofbox', 'concept_wall_left', 'concept_wall_right'])

#['target_left', 'target_above', 'wall_below', 'left_switch', 'target_below', 'empty_right', 'wall_left', 'empty_left', 'box_left', 'above_switch', 'empty_below', 'switch_on', 'wall_above', 'box_right', 'target_right', 'wall_left_below_ofbox', 'empty_above', 'wall_right'])

per_action_ratio = []
for act_id in range(len(concept_dict['act_concept_map'])):
    conc_map = concept_dict['act_concept_map'][act_id]
    total_act_count = concept_dict['action_count'][act_id]
    curr_action_ratio = {}
    for conc in conc_map:
        if conc in concept_set:
            curr_action_ratio[conc] = float(conc_map[conc])/total_act_count
    
    per_action_ratio.append(curr_action_ratio)

per_concept_ratio = {}
total_state_count = concept_dict['total_states']
for conc in concept_dict['concept_count_mark']:
    if conc in concept_set:
        per_concept_ratio[conc] = float(concept_dict['concept_count_mark'][conc])/total_state_count

act_id = 0

for conc_ratio in per_action_ratio:
    #print ("Action ", ACTION_LOOKUP[act_id])
    max_concept = None
    max_diff = 0
    total_diff = 0
    for conc in conc_ratio:
        #print ("Concept",conc,"Observed ratio",conc_ratio[conc], "expected ratio", per_concept_ratio[conc])
        curr_diff = abs(per_concept_ratio[conc] - conc_ratio[conc])
        total_diff += curr_diff
        if curr_diff > max_diff:
            max_diff = curr_diff
            max_concept = conc
    #print ("Concept with maximum difference", max_concept, "absolute difference between the estimates", max_diff)
    print (ACTION_LOOKUP[act_id],"&",max_concept.replace("concept_","").replace("_","\_"),"&",round(max_diff,4),"&",round(total_diff/len(conc_ratio),4),"\\\\")
    act_id += 1
