export TESTCASE4_HOME=$(pwd)
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_thumb >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_thumb/src
mvn package
cd ../scripts/
./action_create.sh
./deploy.sh

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_resize >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_resize/action/
./action_update.sh

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< c_rsa >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd c_rsa/action/
./action_update.sh


echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< data_analysis >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd data_analysis/scripts/
./deploy.sh

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< alloc_res >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd alloc_res/
./action_update.sh