export TESTCASE4_HOME=$(pwd)
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_thumb >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_thumb/src
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 5; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 5; done;
cd ../..
sleep 30


echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< img_resize >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd img_resize/action/
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 2; done;
cd ../..
sleep 30


echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< c_rsa >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd c_rsa/action/
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 1; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 1; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 1; done;
cd ../..
sleep 30



echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< data_analysis >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd data_analysis/scripts/
for f in {1..112}; do echo ========round $f========; ./action_invoke_1.sh $f; sleep 5; done;
for f in {113..224}; do echo ========round $f========; ./action_invoke_2.sh $f; sleep 5; done;
for f in {225..336}; do echo ========round $f========; ./action_invoke_3.sh $f; sleep 5; done;
cd ../..
sleep 30

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<< alloc_res >>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd alloc_res/
for f in {01..112}; do echo ========round $f========; ./action_invoke_1.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_2.sh; sleep 2; done;
for f in {01..112}; do echo ========round $f========; ./action_invoke_3.sh; sleep 2; done;
cd ../..
sleep 30
