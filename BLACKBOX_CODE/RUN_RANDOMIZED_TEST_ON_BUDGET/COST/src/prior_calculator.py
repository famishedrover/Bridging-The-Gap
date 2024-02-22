from .prior_sampler import PriorSampler

import sys

if __name__ == "__main__":

    plan_cost = int(sys.argv[3])
    foil_file = sys.argv[2]
    domain_name = sys.argv[1]
    if len(sys.argv) > 4:
       sampling_budget = int(sys.argv[4])
    else:
       sampling_budget = 50
    exp_obj = PriorSampler(domain_name, foil_file, plan_cost, sampling_budget)
    for cnt in [1000]: #[5, 10, 50, 100, 250, 500, 750, 1000]:
        exp_obj.create_priors(cnt)
        print (exp_obj.executable_state_action_val_prior) 
        print (exp_obj.executable_state_concept_prior) 
