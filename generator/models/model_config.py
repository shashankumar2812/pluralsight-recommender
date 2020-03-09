from generator.data.data_utils import split_with_comma

sim_interest_model_params = {"analyzer": split_with_comma, "min_df": 5}
sim_course_view_params = {"similarity": "cosine", "target": "view_time_seconds"}
sim_course_level_model_params = {
    "embedding_size": 10,
    "regularizer": 0.01,
    "training_stop_accuracy_threshold_callback": 0.997,
    "loss": "sparse_categorical_crossentropy",
    "optimizer": "adam",
    "metrics": ["accuracy"],
    "test_size": 0.1,
    "batch_size": 128,
    "epochs": 50,
}

