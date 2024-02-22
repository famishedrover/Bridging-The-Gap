##### To be filled
ABSOLUTE_TEST = True
ALL_FILES = "all_files"
STR_SEQ_MAP = "STR_SEQ"
STR_CONC_MAP = "STR_CONC"
NEG_CONCEPT_PREFIX = "NOT_"


CONCEPT_CLASS_MAP = {'montezuma': '.concept_class.MontezumaConceptClass.MontezumaConceptClass',
                     'montezumal3': '.concept_class.MontezumaL3ConceptClass.MontezumaL3ConceptClass',
                     'sokoban_flip_prec': 'concept_class.SokobanFlip.SokobanFlipConceptClass'}
SIMULATOR_CLASS_MAP = {'montezuma': '.simulator_classes.MontezumaSimulator.MontezumaSimulator',
                       'montezumal3': '.simulator_classes.MontezumaSimulator.MontezumaSimulator',
                       'sokoban_flip_prec': 'simulator_classes.SokobanFlipSimulator.SokobanFlipSimulator'}


# Test parameters
THRESHOLD_FOR_REMOVAL = 0.05
SAMPLES_BUDGET = 500