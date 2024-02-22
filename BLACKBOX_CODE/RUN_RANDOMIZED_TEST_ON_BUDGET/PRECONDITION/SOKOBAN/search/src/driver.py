import os
import sys
from ConceptLattice import ConceptLattice


if __name__ == '__main__':
    #current_state_ram_file = sys.argv[3]
    domain_name = "sokoban_flip_prec" #sys.argv[4]

    prob_dist = None
    if domain_name == "montezuma":
        prob_dist = {'on_ladder1': 0.2042797805779982, 'on_ladder2': 0.09674196883927164, 'on_ladder3': 0.2060411153367567, 'on_middle_platform': 0.07145892847754079, 'on_rope': 0.014285651693860741, 'on_ground_and_alive': 0.09426207960181567, 'skull_on_right': 0.0005564415780157381, 'skull_on_left': 0.0005739672970083597, 'on_highest_platform': 0.0032970258854869523, 'die_on_left': 0.007717888501375769}
    elif domain_name == "montezumal3":
        prob_dist = {'onLeftPassage': 0.04665315690173234, 'crabLiesToRight': 0.2079317989797798, 'onLadderTop': 0.13215218178468655, 'onLadderBottom': 0.7125659871551357, 'isClearDownCrab': 0.8466144063220618, 'onRightPassage': 0.09305221164169054, 'inAir': 0.09354453458012794, 'onLadder': 0.8469225051932129, 'crabLiesToLeft': 0.6727831174523717, 'isClearUpCrab': 0.8466620504773944}

    elif domain_name == 'sokoban_flip_prec':
        prob_dist = {'concept_above_switch': 0.04491893228990983, 'concept_box_above': 0.06614720366997234, 'concept_box_below': 0.01892329487957903,
                     'concept_box_left': 0.037914052486001486, 'concept_box_right': 0.02794081270098271, 'concept_empty_above': 0.7423823337605973,
                     'concept_empty_below': 0.5689581506217815, 'concept_empty_left': 0.6626526344194832, 'concept_empty_right': 0.5740965616496886,
                     'concept_left_switch': 0.07128561469787942, 'concept_order_T2D_target_box_player': 0.00861274146034316,
                     'concept_switch_on': 0.7202995345071848, 'concept_target_above': 0.017787672311048146, 'concept_target_below': 0.008680204187186579,
                     'concept_target_left': 0.011131349929164137, 'concept_target_right': 0.011367469473116103,
                     'concept_wall_above': 0.17368279025838224, 'concept_wall_below': 0.3585194180215431,
                     'concept_wall_left': 0.2883019631653511, 'concept_wall_left_below_ofbox': 0.013571251883334457,
                     'concept_wall_right': 0.31530954147833323}

    starting_concepts = ['concept_box_above', 'concept_empty_left', 'concept_empty_right']
    foil_act = 1 #sys.argv[2]

    budget_list = [5, 10, 100, 250, 500, 750, 1000]
    #budget_list = [5]
    #for cnt in [5, 10, 100, 250, 500, 750, 1000]:
    lat_obj = ConceptLattice(foil_act, starting_concepts=starting_concepts, domain_name=domain_name, prob_dist=prob_dist)
    lat_obj.search_from_files(current_sampling_budget_list=budget_list)
