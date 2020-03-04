import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ..data.data_utils import create_user_indices_from_user_handle
from DEFAULTS import NUM_SIMILAR_USERS

logger = logging.getLogger(__name__)

class SimilarInterestUserModel:
    def __init__(self, **params):
        logger.info('Entering Class {} '.format(self.__class__.__name__))
        self.params=params
        self.data=None
        self.X=None
        self.user_index_dict={}
    
    def fit(self, data): 
        logger.debug('Entering fit method of class {} '.format(self.__class__.__name__))
        self.data=data
        self.user_index_dict=create_user_indices_from_user_handle(self.data)
        tf_vectorizer = TfidfVectorizer(self.params)
        self.X = tf_vectorizer.fit_transform(self.data.interest_tag)
        logger.debug('Finished running fit method of class {} '.format(self.__class__.__name__))
        return self
    
    def predict_similar_users(self, user_handle, num_similar_users=NUM_SIMILAR_USERS):
        logger.debug(f'Predicting similar users for user_handle {user_handle}')
        user=self.user_index_dict[user_handle]
        cosine_similarities = linear_kernel(self.X[user], self.X).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-num_similar_users:-1]
        data = {'similar_users':self.data.loc[related_docs_indices].user_handle.values, 
                'interest_sim_score':cosine_similarities[related_docs_indices]} 
        logger.debug(f'Predictions for user_handle {user_handle} {data}')
        logger.debug(f'Predicted similar users for {user_handle}')
        return pd.DataFrame(data)