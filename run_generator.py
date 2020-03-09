from datetime import datetime
import logging
from db_utils import create_table
from DEFAULTS import GEN_LOG_LEVEL
from generator.data.process_data import (
    UserInterestDataProcessor,
    UserCourseViewTimeDataProcessor,
    UserCourseLevelDataProcessor,
)
from generator.models.model_config import (
    sim_interest_model_params,
    sim_course_view_params,
    sim_course_level_model_params,
)
from db_writer import run_similar_user_generator
from generator.models.similar_interest_model import SimilarInterestUserModel
from generator.models.similar_view_time_model import UserCourseViewSimilarityCFModel
from generator.models.similar_user_level_model import (
    UserCourseLevelViewSimilarityCFModel,
)
from helpers.utils import log_exception
from paths import generator_log_file

logger = logging.getLogger(__name__)


def main():
    try:
        start_time = datetime.now()
        logger.info("Starting Iris!")
        create_table()
        run_similar_user_generator(
            SimilarInterestUserModel,
            sim_interest_model_params,
            UserInterestDataProcessor,
            model_handle="tfidf_user_interest",
        )
        run_similar_user_generator(
            UserCourseViewSimilarityCFModel,
            sim_course_view_params,
            UserCourseViewTimeDataProcessor,
            model_handle="knn_collab_filtering_user_course_view",
        )
        run_similar_user_generator(
            UserCourseLevelViewSimilarityCFModel,
            sim_course_level_model_params,
            UserCourseLevelDataProcessor,
            model_handle="dnn_collab_filtering_user_course_level",
        )
        logger.info("Iris Done Generating Similar Users!")
        logger.info(
            "Time of running the script: {}".format(datetime.now() - start_time)
        )
    except:
        log_exception()


if __name__ == "__main__":
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(generator_log_file, mode="w"),
            logging.StreamHandler(),
        ],
        level=GEN_LOG_LEVEL,
    )
    main()
