from generator.data.data_utils import split_with_comma

sim_interest_model_params = {"analyzer": split_with_comma, "min_df": 5}
sim_course_view_params = {"similarity": "cosine", "target": "view_time_seconds"}

