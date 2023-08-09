export TESTCASE4_HOME=$(pwd)
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_thumb >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_thumb/src
mvn package
cd ../scripts/
./action_create.sh
./deploy.sh
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 5; done;
cd ../..
sleep 30


echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_resize >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_resize/action/
./action_update.sh
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 2; done;
cd ../..
sleep 30


echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< c_rsa >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd c_rsa/action/
./action_update.sh
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 1; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 1; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 1; done;
cd ../..
sleep 30



echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< data_analasys >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd data_analysis/scripts/
./deploy.sh
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 5; done;
cd ../..
sleep 30

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< alloc_res >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd alloc_res/
./action_update.sh
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 2; done;
cd ../..
sleep 30
