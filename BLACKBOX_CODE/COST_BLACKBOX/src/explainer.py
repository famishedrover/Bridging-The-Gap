from .cost_explainer import CostExplanation

import sys

if __name__ == "__main__":

    plan_cost = int(sys.argv[3])
    foil_file = sys.argv[2]
    domain_name = sys.argv[1]
    exp_obj = CostExplanation(domain_name, foil_file, plan_cost)

    explanation = exp_obj.find_concept_set_prioritize_number_of_concepts()
    print ("explanation", explanation)