# CONCEPT_NAME = "concept_box_above"
# CONCEPT_NAME = "concept_box_left"
seed = 20

ROOT = "runs-power-flip-cost"
EPOCHS = 60
BATCH_SIZE = 16

# NEG_LIMIT = 1000
# POS_LIMIT = 1000
# TRAIN_RATIO = 0.1

COUNT_THRESHOLD = 200 


# for rest of the concepts > 200 pos examples 
NEG_LIMIT = 60
POS_LIMIT = 30
TRAIN_RATIO = 0.7



# # for concept_box_below
# NEG_LIMIT = 150
# POS_LIMIT = 33
# TRAIN_RATIO = 0.8


# # for concept_box_above
# NEG_LIMIT = 80
# POS_LIMIT = 26
# TRAIN_RATIO = 0.8
# # [[31.  0.]
# #  [ 2.  3.]]
# # DATESET -- 
# # Train  140 Test  36
# # In Train : 
# # Accuracy of the network on test images: 94 %
# # Finished Training
# # {'concept_box_below': 94.44444444444444}




SELECT_POSSIBLE = True
SEED = 3




# ep[ 202 / 1000 ]   Count pos/neg/actualneg
# {'concept_above_switch': [17, 168, 603],
#  'concept_below_switch': [0, 0, 620],
#  'concept_box_above': [27, 234, 593],
#  'concept_box_below': [20, 196, 600],
#  'concept_box_left': [15, 189, 605],
#  'concept_box_right': [16, 171, 604],
#  'concept_empty_above': [462, 156, 158],
#  'concept_empty_below': [431, 188, 189],
#  'concept_empty_left': [406, 214, 214],
#  'concept_empty_right': [398, 222, 222],
#  'concept_left_switch': [20, 201, 600],
#  'concept_orderL2R_player_box_target': [0, 0, 620],
#  'concept_orderL2R_target_box_player': [0, 0, 620],
#  'concept_order_T2D_target_box_player': [2, 70, 618],
#  'concept_right_switch': [0, 0, 620],
#  'concept_switch_on': [160, 297, 460],				100 percent
#  'concept_target_above': [20, 198, 600],
#  'concept_target_below': [14, 164, 606],
#  'concept_target_left': [22, 188, 598],
#  'concept_target_right': [17, 171, 603],
#  'concept_wall_above': [111, 373, 509],
#  'concept_wall_below': [138, 439, 482],
#  'concept_wall_left': [177, 440, 443],
#  'concept_wall_left_below_ofbox': [36, 229, 584],
#  'concept_wall_right': [169, 435, 451]}



# ep[ 231 / 1000 ]   Count pos/neg/actualneg
# Run Save runs-flip 05/07 1349hrs
# {'concept_box_above': [2325, 13314, 25395],
#  'concept_box_below': [1016, 9315, 26704],
#  'concept_switch_on': [3811, 15754, 23909]}
# seed = 20



# ep[ 201 / 1000 ]   Count pos/neg/actualneg
# {'concept_above_switch': [533, 5690, 22564],
#  'concept_below_switch': [0, 0, 23097],
#  'concept_box_above': [2110, 11703, 20987],
#  'concept_box_below': [669, 6936, 22428],
#  'concept_box_left': [826, 7241, 22271],
#  'concept_box_right': [1068, 8610, 22029],
#  'concept_empty_above': [17999, 5095, 5098],
#  'concept_empty_below': [13747, 9329, 9350],
#  'concept_empty_left': [14561, 8536, 8536],
#  'concept_empty_right': [14948, 8149, 8149],
#  'concept_left_switch': [915, 7927, 22182],
#  'concept_orderL2R_player_box_target': [0, 0, 23097],
#  'concept_orderL2R_target_box_player': [0, 0, 23097],
#  'concept_order_T2D_target_box_player': [96, 2167, 23001],
#  'concept_right_switch': [0, 0, 23097],
#  'concept_switch_on': [2712, 12765, 20385],
#  'concept_target_above': [492, 5989, 22605],
#  'concept_target_below': [224, 3687, 22873],
#  'concept_target_left': [412, 5116, 22685],
#  'concept_target_right': [297, 4179, 22800],
#  'concept_wall_above': [2496, 12525, 20601],
#  'concept_wall_below': [7924, 15167, 15173],
#  'concept_wall_left': [7298, 15775, 15799],
#  'concept_wall_left_below_ofbox': [569, 6186, 22528],
#  'concept_wall_right': [5869, 17191, 17228]}


