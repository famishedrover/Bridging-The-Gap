domain=$1
foil=$2
mkdir -p ../LOGS/${domain}/${foil}/
pushd ../search/src/
python driver.py $domain $foil |grep "LOGS"  > ../../LOGS/${domain}/${foil}/log.log
popd
