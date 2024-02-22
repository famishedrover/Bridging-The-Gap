Setting up the environment
----
OS tested on 
"Ubuntu 14.04.5 LTS"
---
Anaconda setup command and basic packages:
        conda create -n expenv python=3.6
        conda activate expenv
        pip install gym==0.17.1
        pip install matplotlib==3.2.1
        pip install pyyaml
        pip install atari_py
        pip install sklearn
        pip install torch==1.5.0
        pip install torchvision==0.6.0
        pip install numpy==1.18.3


----
Steps:


Let $CODE_DIR be the root directory where the code was checked out


----
Installing basic environments:
        cd $CODE_DIR/SOKOBAN_ENVS/gym-sokoban_gravity_cost/
        python setup.py develop
        cd $CODE_DIR/SOKOBAN_ENVS/gym-sokoban_switch/
        python setup.py develop
        cd $CODE_DIR/SOKOBAN_ENVS/gym-sokoban_power_flip/
        python setup.py develop

------
Training Models for PRECONDITIONS:


$CODE_DIR/PRECOND_BLACKBOX/requirements.txt has the list of python packages required for running scripts for training models for PRECONDITION task.


First we need to sample positive and negative examples. For that we run the samplers.


>>> LEVEL 1 : Montezuma

        cd $CODE_DIR/PRECOND_BLACKBOX/sampler_and_conceptTrain
        python -m sampling.sampler --level 1
Code Saves the concepts at CODE_DIR/PRECOND_BLACKBOX/sampler_and_conceptTrain/concepts


The code creates a folder named concept where positive and negative examples of concepts would be saved for each concept. 
Directories : 
“PRECOND_BLACKBOX/sampler_and_conceptTrain/cases”
“PRECOND_BLACKBOX/sampler_and_conceptTrain/cases/myconcepts” should also exist.


>>> LEVEL 4 : Montezuma

        cd $CODE_DIR/PRECOND_BLACKBOX/sampler_and_conceptTrain
        python -m sampling.sampler --level 4

Code Saves the concepts at CODE_DIR/PRECOND_BLACKBOX/sampler_and_conceptTrain/myconcept/level3_run7


The code creates a folder named concept where positive and negative examples of concepts would be saved for each concept. 
Directories : 
“PRECOND_BLACKBOX/sampler_and_conceptTrain/cases”
“PRECOND_BLACKBOX/sampler_and_conceptTrain/cases/myconcepts” sho


Now we can Train the Classifiers : Montezuma
        
cd $CODE_DIR/PRECOND_BLACKBOX/sampler_and_conceptTrain/conceptTraining
        python train.py --level 4
Or 
python train.py --level 1


You can provide path to a custom concept folder (if you change the default names in the .py scripts)
        python train.py --root <root-path>






Training Models for COST:


        For sokoban-cell:
        1. cd $CODE_DIR/COST_TRAINER/SOKOBAN_CELL_TRAINER/
        2. python sample_concept_states_cell.py
        3. python trainer.py
        4. Copy the models to the search directory
                cp $CODE_DIR/COST_TRAINER/SOKOBAN_CELL_TRAINER/runs-power-flip-cost/models/* $CODE_DIR/COST_BLACKBOX/src/DATA/GRAVITY_MODELS/




        For sokoban-switch:
        1. cd $CODE_DIR/COST_TRAINER/SOKOBAN_SWITCH_TRAINER/
        2. python sample_concept_states_switch.py
        3. python trainer.py
        4. Copy the models to the search directory
                cp $CODE_DIR/COST_TRAINER/SOKOBAN_SWITCH_TRAINER/runs-power-flip-cost/models/* $CODE_DIR/COST_BLACKBOX/src/DATA/FLIP_MODELS/


        


------
Precondition identification

Montezuma:

Running the search:


1. Run the sampler to create the set of possible samples
        mkdir -p /tmp/ProjectsData/blackBoxExp/
        Sample for Level1
        1. go to sample directory
                cd $CODE_DIR/PRECOND_BLACKBOX/sampler_code/level1_sampler/
        2. Run the sampler
                    python sampler.py
        3. mv /tmp/ProjectsData/blackBoxExp/samples/*  $CODE_DIR/PRECOND_BLACKBOX/DATA/SAMPLES/MONTEZUMA/


        Sample for Level4
        1. go to sample directory
                cd $CODE_DIR/PRECOND_BLACKBOX/sampler_code/level4_sampler/
        2. Run the sampler
                    python sampler.py
        3. mv /tmp/ProjectsData/blackBoxExp/samples/*  $CODE_DIR/PRECOND_BLACKBOX/DATA/SAMPLES/MONTEZUMAL4/


2. Run the search
        cd $CODE_DIR/PRECOND_BLACKBOX/search_code/
        python driver.py ${domain_name} ${foilid}
        ----
        Where $domain_name could be montezuma montezumal4
        $foilid could foil1 foil2 and foil3 for montezuma and foil1 for montezumal4 


Sokoban:
1. Run the sampler to create the set of possible samples
    1. go to sample directory
                cd $CODE_DIR/PRECOND_BLACKBOX/sampler_code/sokoban_sampler/
    2. Run the sampler
                python sample_concept_states_switch_samples_dir.py
    3. Move the '*.seq' samples at runs-power-flip-cost/samples to /tmp/sokoban_switch_samples/

2. Run the search
    1. go to search directory
        cd $CODE_DIR/PRECOND_BLACKBOX/search_code_for_sokoban
        python driver.py



------
Cost function identification:


1. Run the sampler to create the set of possible samples
        To create the sampled for sokoban_cell        
                mkdir -p $CODE_DIR/COST_BLACKBOX/src/DATA/GRAVITY_SAMPLES/CONCEPT_MAP/
                cd $CODE_DIR/COST_BLACKBOX/src/sampler/
                python sample_sokoban_cell.py
        
        To create the sampled for sokoban_switch
                mkdir -p $CODE_DIR/COST_BLACKBOX/src/DATA/FLIP_SAMPLES/CONCEPT_MAP/
                cd $CODE_DIR/COST_BLACKBOX/src/sampler/
                python sample_sokoban_switch.py


2. Go to the experiment script directory and run the specific script
        cd $CODE_DIR/COST_BLACKBOX/experiment_scripts
        
        To generate explanation for sokoban-cell
                ./run_simulator_cell.sh 


        To generate explanation for sokoban-switch
                ./run_simulator_switch.sh

---
Running the code to test assumptions:

1. Go to $CODE_DIR/ASSUMPTION_ANALYSIS_CODE/ directory
2. Each subdirectory here correspond to a specific variant on which the corresponding analysis was run
3. In each directory first run the code sample_concept_for_analysis.py which will create a yaml that contains the results of the sampling performed on the domain
4. Next run the code analyze_prob_of_concepts_considered.py to see the results of the analysis


---
Running the code for randomized experiment for budget comparison

PRECONDITION_CODE (Here level 4 was mapped to l3)
Montezuma 
1. Per earlier steps copy samples to $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/MONTEZUMA/DATA/SAMPLES/MONTEZUMA/ and $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/MONTEZUMA/DATA/SAMPLES/MONTEZUMAL3/
2. go to $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/MONTEZUMA/scripts/
3. For Level1 run   `./run_randomized_experiment.sh montezuma $id` where $id could be 1 2 or 3
4. For Level4 run   `./run_randomized_experiment.sh montezumal3 $id` where $id should be 1
5. The results would be saved in  $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/MONTEZUMA/LOGS/

Sokoban 
1. Per earlier step create samples for SOKOBAN_FLIP and copy just the '.seq' files to $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/SOKOBAN/DATA/SAMPLES/SOKOBAN/
2. go to $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/SOKOBAN/scripts/
3. Run `./run_randomized_experiment.sh`
4. The results would be saved in  $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/PRECONDITION/SOKOBAN/LOGS/

COST
Sokoban
1. Make samples for both variants according to the earlier step (the sampler location now being $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/COST/src/sampler/)
2. Go to  $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/COST/experiment_scripts/
3. For sokoban_switch run `./run_simulator_flip_multiple_budget.sh`, the results will be saved in $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/COST/LOGS_FLIP
3. For sokoban_cell run `./run_simulator_gravity_multiple_budget.sh`, the results will be saved in $CODE_DIR/RUN_RANDOMIZED_TEST_ON_BUDGET/COST/LOGS_GRAVITY
