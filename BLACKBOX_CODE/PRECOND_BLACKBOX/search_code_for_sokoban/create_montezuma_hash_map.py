import os
import sys
from constants  import *
import yaml
import pickle
from concept_class.MontezumaConceptClass import MontezumaConceptClass

dst_file = sys.argv[1]
SAMPLES_DIR = "../DATA/SAMPLES/MONTEZUMA/"
RAM_NAME = "sample_RAM.b"
ACTION_SEQ = "sample_action_seq.b"

concept_class_obj = MontezumaConceptClass()
hash_map = {}

hash_map[ALL_FILES] = set()
hash_map[STR_SEQ_MAP] = {}
hash_map[STR_CONC_MAP] = {}

for root, dirs, files in os.walk(SAMPLES_DIR):
    for sdir in dirs:
        print (sdir)
        hash_map[ALL_FILES].add(sdir)
        current_sample_dir = os.path.join(SAMPLES_DIR, sdir)
        with open(os.path.join(current_sample_dir, RAM_NAME), 'rb') as r_fd:
            ram_state = pickle.load(r_fd)
        with open(os.path.join(current_sample_dir, ACTION_SEQ), 'rb') as a_fd:
            act_seq = pickle.load(a_fd)
        valid_concepts = concept_class_obj.get_all_valid_concepts(ram_state)
        #print (valid_concepts)
        hash_map[STR_CONC_MAP][sdir] = set()
        for conc in valid_concepts:
            if conc not in hash_map:
                hash_map[conc] = set()
            hash_map[conc].add(sdir)
            hash_map[STR_CONC_MAP][sdir].add(conc)
        hash_map[STR_SEQ_MAP][sdir] = act_seq

with open(dst_file, 'w') as d_fd:
    yaml.dump(hash_map, d_fd)
