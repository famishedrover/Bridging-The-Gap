mkdir -p ../LOGS/
pushd ../search/src
python driver.py |grep "LOGS" > ../../LOGS/log.log
popd
