pushd ../
mkdir -p LOGS_FLIP/
for s in 0 1 2 3 4 5 6 7 8 9 #5 10 50 100 250 500 750 1000
do
    python -m src.explainer sokoban-flip /home/yochan/mycode/blackboxexp/COST_EXPLANATION/experiment_scripts/scenario_flip/foil1_cost 5 $s > LOGS_FLIP/log.${s}
done
popd
