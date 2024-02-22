import json
import sys

js_file = sys.argv[1]
with open(js_file) as j_fd:
     explanation_dump = json.load(j_fd)

concept_explanation_steps = []
saliency_explanation_steps = []
concept_explanation_time = []
saliency_explanation_time = []

print ("Total number of responses", len(explanation_dump['users_info']))
men_count = 0
women_count = 0
ai_known = 0
planning_known = 0
for k in explanation_dump['users_info']:
    if explanation_dump['users_info'][k]['explanation_seen'] == 'yes':
        if explanation_dump['users_info'][k]['gender'] == 'female':
            women_count +=1
        if explanation_dump['users_info'][k]['gender'] == 'male':
            men_count +=1
        if explanation_dump['users_info'][k]['ai_knowledge'] == 'yes':
            ai_known +=1
        if explanation_dump['users_info'][k]['plan_knowledge'] == 'yes':
            planning_known +=1
        if explanation_dump['users_info'][k]['explanation_type'] == 'concept':
            concept_explanation_steps.append(explanation_dump['users_info'][k]['steps_taken'])
            concept_explanation_time.append(int(explanation_dump['users_info'][k]['minutes'])*60+int(explanation_dump['users_info'][k]['seconds']))
        elif explanation_dump['users_info'][k]['explanation_type'] == 'saliency':
            saliency_explanation_steps.append(explanation_dump['users_info'][k]['steps_taken'])
            saliency_explanation_time.append(int(explanation_dump['users_info'][k]['minutes'])*60+int(explanation_dump['users_info'][k]['seconds']))


print ("Male count", men_count)
print ("Female count", women_count)
print ("ai count", ai_known)
print ("plan count", planning_known)

print ("No of concept explanations",len(concept_explanation_steps))
print ("Concept Explanation steps")

for steps in concept_explanation_steps:
    print (steps)

print ("Concept Explanation time")

for exp_time in concept_explanation_time:
    print (exp_time)


print ("No of saliency explanations",len(saliency_explanation_steps))
print ("Concept Explanation steps")

for steps in saliency_explanation_steps:
    print (steps)

print ("Concept Explanation time")

for exp_time in saliency_explanation_time:
    print (exp_time)
