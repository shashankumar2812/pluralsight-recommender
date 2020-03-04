import heapq
import logging
import pandas as pd
from surprise import KNNBasic
from ..data.data_utils import create_surprise_data_set
from DEFAULTS import NUM_SIMILAR_USERS
from helpers.utils import log_exception

logger = logging.getLogger(__name__)


class UserCourseViewSimilarityCFModel:
    def __init__(self, **params):
        logger.info("Entering Class {} ".format(self.__class__.__name__))
        self.params = params
        self.sim_options = {"name": self.params["similarity"], "user_based": True}
        self.algo = KNNBasic(sim_options=self.sim_options)
        self.target = self.params["target"]
        self.data = None
        self.surprise_data_set = None
        self.sims_matrix = None

    def fit(self, data):
        logger.debug("Entering fit method of class {} ".format(self.__class__.__name__))
        self.data = data
        self.surprise_data_set = create_surprise_data_set(self.data, self.target)
        self.algo.fit(self.surprise_data_set)
        self.sims_matrix = self.algo.compute_similarities()
        logger.debug(
            "Finished running fit method of class {} ".format(self.__class__.__name__)
        )
        return self

    def predict_similar_users(self, user_handle, num_similar_users=NUM_SIMILAR_USERS):
        try:
            logger.debug(f"Predicting similar users for user_handle {user_handle}")
            user_handle_inner_id = self.surprise_data_set.to_inner_uid(user_handle)
            similarity_row = self.sims_matrix[user_handle_inner_id]
            similar_users = []
            for inner_id, score in enumerate(similarity_row):
                if inner_id != user_handle_inner_id:
                    similar_users.append((inner_id, score))
            k_neighbors = heapq.nlargest(
                num_similar_users, similar_users, key=lambda t: t[1]
            )
            data = [
                (self.surprise_data_set.to_raw_uid(user[0]), user[1])
                for user in k_neighbors
            ]
            logger.debug(f"Predictions for user_handle {user_handle} {data}")
            logger.debug(f"Predicted similar users for {user_handle}")
            return pd.DataFrame(data, columns=["similar_users", "view_time_sim_score"])
        except KeyError:
            log_exception()
