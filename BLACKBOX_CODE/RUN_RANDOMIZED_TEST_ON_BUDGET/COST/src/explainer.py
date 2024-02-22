from .cost_explainer import CostExplanation

import sys

if __name__ == "__main__":

    plan_cost = int(sys.argv[3])
    foil_file = sys.argv[2]
    domain_name = sys.argv[1]
    if len(sys.argv) > 4:
       sampling_budget = int(sys.argv[4])
    else:
       sampling_budget = 50
    exp_obj = CostExplanation(domain_name, foil_file, plan_cost, sampling_budget)
    for cnt in [5, 10, 50, 100, 250, 500, 750, 1000]: #[5, 10, 50, 100, 250, 500, 750, 1000]:
        explanation, prob = exp_obj.find_concept_set_prioritize_number_of_concepts(cnt)
        #print ("explanation", explanation)
        #print (exp_obj.executable_state_action_val_prior) 
        #print (exp_obj.executable_state_concept_prior) 
        #print (exp_obj.executable_state_cost_map)
        print (str(cnt)+":PROB>>>> ", prob)
