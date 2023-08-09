wsk -i action create linpack linpack/linpack.py --docker shariar076/python3aiaction --timeout 300000
wsk -i action create matmul matmul/matmul.py --docker shariar076/python3aiaction --timeout 300000
wsk -i action create float_operation float_operation/float_operation.py --docker shariar076/python3aiaction --timeout 300000
wsk -i action create chameleon chameleon/chameleon_test.py --docker shariar076/python3action-chameleon --timeout 300000
wsk -i action create video_processing video_processing/video_processing.py --docker shariar076/python3aiaction --timeout 300000

cd image_processing
rm -f image_processing.zip
cp image_processing.py __main__.py
zip -r image_processing.zip __main__.py ops.py
wsk -i action create image_processing image_processing.zip --docker shariar076/python3aiaction --timeout 300000
cd ../

wsk -i action create model_training model_training/model_training.py --docker shariar076/python3aiaction --timeout 300000

wsk -i action create pyaes pyaes/pyaes_test.py --docker shariar076/python3action-pyaes --timeout 300000

wsk -i action create feature_extractor feature_generation/feature_extractor.py --docker shariar076/python3aiaction --timeout 300000
wsk -i action create feature_reducer feature_generation/feature_reducer.py --docker shariar076/python3aiaction --timeout 300000
wsk -i action create orchestrator feature_generation/orchestrator.py --timeout 300000
wsk -i action create get_job_status feature_generation/get_job_status.py --timeout 300000

wsk -i action create mapper mapreduce/mapper.py --timeout 300000
wsk -i action create reducer mapreduce/reducer.py --timeout 300000
wsk -i action create driver mapreduce/driver.py --timeout 300000

cd cnn_image_classification
rm -f cnn_image_classification.zip
cp cnn_image_classification.py __main__.py
zip -r cnn_image_classification.zip __main__.py squeezenet.py
wsk -i action create cnn_image_classification cnn_image_classification.zip --docker shariar076/python3aiaction --timeout 300000
cd ..

wsk -i action create ml_lr_prediction ml_lr_prediction/ml_lr_prediction.py --docker shariar076/python3aiaction --timeout 300000

wsk -i action create ml_video_face_detection ml_video_face_detection/ml_video_face_detection.py --docker shariar076/python3aiaction --timeout 300000

cd rnn_generate_character_level
rm -f rnn_generate_character_level.zip
cp rnn_generate_character_level.py __main__.py
zip -r rnn_generate_character_level.zip __main__.py rnn.py
wsk -i action create rnn_generate_character_level rnn_generate_character_level.zip --docker shariar076/python3aiaction --timeout 300000
cd ..
