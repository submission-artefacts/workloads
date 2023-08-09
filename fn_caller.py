import json
import os
import sys

sys.path.append(os.path.abspath('./functionbench/image_processing'))
sys.path.append(os.path.abspath('./functionbench/cnn_image_classification'))
sys.path.append(os.path.abspath('./functionbench/rnn_generate_character_level'))

sys.path.append(os.path.abspath('./serverlessbench/alloc_res'))

payloads = json.load(open('./payloads.json'))


def call(fn_name, rep):
    if fn_name == 'linpack':
        from functionbench.linpack.linpack import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'matmul':
        from functionbench.matmul.matmul import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'chameleon':
        from functionbench.chameleon.chameleon_test import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'video_processing':
        from functionbench.video_processing.video_processing import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'image_processing':
        from functionbench.image_processing.image_processing import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'model_training':
        from functionbench.model_training.model_training import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'pyaes':
        from functionbench.pyaes.pyaes_test import main
        return main(payloads[fn_name][rep])

    elif fn_name=='orchestrator':
        from functionbench.feature_generation.orchestrator import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'feature_extractor':
        from functionbench.feature_generation.feature_extractor import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'feature_reducer':
        from functionbench.feature_generation.feature_reducer import main
        return main(payloads[fn_name][rep])

    # elif fn_name=='get_job_status':
    #     from functionbench.feature_generation.get_job_status import main
    #     return main(payloads[fn_name][rep])

    elif fn_name=='driver':
        from functionbench.mapreduce.driver import main
        return main(payloads[fn_name][rep])
    elif fn_name == 'mapper':
        from functionbench.mapreduce.mapper import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'reducer':
        from functionbench.mapreduce.reducer import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'cnn_image_classification':
        from functionbench.cnn_image_classification.cnn_image_classification import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'ml_lr_prediction':
        from functionbench.ml_lr_prediction.ml_lr_prediction import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'ml_video_face_detection':
        from functionbench.ml_video_face_detection.ml_video_face_detection import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'rnn_generate_character_level':
        from functionbench.rnn_generate_character_level.rnn_generate_character_level import main
        return main(payloads[fn_name][rep])

    elif fn_name == 'float_operation':
        from functionbench.float_operation.float_operation import main
        return main(payloads[fn_name][rep])

    elif fn_name == "alloc_res":
        from serverlessbench.alloc_res.alloc_res import main
        main(payloads[fn_name][rep])


if __name__ == "__main__":
    call("alloc_res", 2)
    # fn_list = ["linpack", "matmul", "chameleon", "video_processing", "image_processing",
    #            "model_training", "pyaes", "feature_extractor", "feature_reducer", "mapper",
    #            "reducer", "cnn_image_classification", "ml_lr_prediction", "ml_video_face_detection",
    #            "rnn_generate_character_level", "float_operation"]
    # for fn in fn_list:
    #     print("=" * 10, fn, "=" * 10)
    #     res = call(fn, 0)
    #     print("Success", type(res) == dict)
