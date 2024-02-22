pushd ../
mkdir -p LOGS_GRAVITY/
for s in 0 1 2 3 4 5 6 7 8 9 #10 50 100 250 500 750 1000
do
    python -m src.explainer sokoban-gravity /home/yochan/mycode/blackboxexp/COST_EXPLANATION/experiment_scripts/scenario_gravity/foil1_cost 9 $s > LOGS_GRAVITY/log.${s}
done
popd
