import os
import sys
from ConceptLattice import ConceptLattice


if __name__ == '__main__':
    concept_map_file = None #sys.argv[1]
    domain_name = sys.argv[1]
    foil_id = sys.argv[2]
    print ("[LOGS] Running for domain",domain_name," and foil", foil_id)
#current_state_ram_file = sys.argv[3]
    #domain_name = "montezuma" #sys.argv[4]
    #domain_name = "montezumal4" #sys.argv[4]

    prob_dist = None
    if domain_name == "montezuma":
        prob_dist = {'on_ladder1': 0.2042797805779982, 'on_ladder2': 0.09674196883927164, 'on_ladder3': 0.2060411153367567, 'on_middle_platform': 0.07145892847754079, 'on_rope': 0.014285651693860741, 'on_ground_and_alive': 0.09426207960181567, 'skull_on_right': 0.0005564415780157381, 'skull_on_left': 0.0005739672970083597, 'on_highest_platform': 0.0032970258854869523, 'die_on_left': 0.007717888501375769}
        foil_act = 4
        if foil_id == '1':
            starting_concepts = ['skull_on_left', 'on_ground_and_alive']
            target_concept = "NOT_skull_on_left"
        elif foil_id == '2':
            starting_concepts = ['on_rope']
            target_concept = "NOT_on_rope"
        elif foil_id == '3':
            starting_concepts = ['on_middle_platform', 'die_on_left']
            target_concept = "NOT_die_on_left"

    elif domain_name == "montezumal4":
        prob_dist = {'onLeftPassage': 0.04665315690173234, 'crabLiesToRight': 0.2079317989797798, 'onLadderTop': 0.13215218178468655, 'onLadderBottom': 0.7125659871551357, 'isClearDownCrab': 0.8466144063220618, 'onRightPassage': 0.09305221164169054, 'inAir': 0.09354453458012794, 'onLadder': 0.8469225051932129, 'crabLiesToLeft': 0.6727831174523717, 'isClearUpCrab': 0.8466620504773944}
        starting_concepts = ['onLadderTop', 'onLadder', 'isClearUpCrab']
        foil_act = 5
        target_concept = 'isClearDownCrab'
    #with open(current_state_ram_file) as c_fd:
    #    current_state = c_fd.read()

    # # Foil 1
    #starting_concepts = ['onLadderTop', 'onLadder', 'isClearUpCrab']
    #starting_concepts = ['skull_on_left', 'on_ground_and_alive']
    #foil_act = 5 #sys.argv[2]
    #foil_act = 4 #sys.argv[2]

    # # Foil 2
    #starting_concepts = ['on_middle_platform', 'die_on_left']
    #starting_concepts = ['on_rope']
    #starting_concepts = ['skull_on_left', 'on_ground_and_alive']
    #foil_act = 4 #sys.argv[2]




    # # Foil 3
    #starting_concepts = ['skull_on_left', 'on_ground_and_alive']
    #foil_act = 4

    # # Foil 4
    # starting_concepts = ['skull_on_left', 'on_ground_and_alive']

    # # Foil 5
    # starting_concepts = ['skull_on_left', 'on_ground_and_alive']

    lat_obj = ConceptLattice(concept_map_file, foil_act, [5, 10, 100, 250, 500, 750, 1000], starting_concepts=starting_concepts, domain_name=domain_name, prob_dist=prob_dist)
    #lat_obj = ConceptLattice(concept_map_file, foil_act, [5], starting_concepts=starting_concepts, domain_name=domain_name, prob_dist=prob_dist)
    #for i in [5, 10, 100, 250, 500, 750, 1000]:
    lat_obj.search_from_files(target_concept)
