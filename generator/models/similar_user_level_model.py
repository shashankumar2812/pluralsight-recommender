import heapq
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from ..data.data_utils import create_user_indices_from_user_handle
from .keras_utils import cp_callback, tensorboard_callback, train_stop_callback
from DEFAULTS import NUM_SIMILAR_USERS

logger = logging.getLogger(__name__)


class UserCourseLevelViewSimilarityCFModel:
    def __init__(self, data, **params):
        self.data = data
        self.params = params
        self.model = None
        self.user_handle_dict = create_user_indices_from_user_handle(self.data)
        self.reverse_user_handle_dict = {
            val: key for key, val in self.user_handle_dict.items()
        }
        self.num_users = self.data.user.max()
        self.num_courses = self.data.course.max()
        self.build_model()

    def build_model(self):
        user = tf.keras.layers.Input(shape=(1,))
        course = tf.keras.layers.Input(shape=(1,))
        embedding_size = self.params["embedding_size"]
        reg = self.params["regularizer"]
        user_emb = tf.keras.layers.Embedding(
            self.num_users + 1,
            embedding_size,
            name="user_embedding",
            embeddings_regularizer=tf.keras.regularizers.l2(reg),
        )(
            user
        )  # (N,1,k)
        user_emb = tf.keras.layers.Flatten()(user_emb)
        course_emb = tf.keras.layers.Embedding(
            self.num_courses + 1,
            embedding_size,
            name="course_embedding",
            embeddings_regularizer=tf.keras.regularizers.l2(reg),
        )(
            course
        )  # (N,1,k)
        course_emb = tf.keras.layers.Flatten()(course_emb)
        concat = tf.keras.layers.concatenate(
            [user_emb, course_emb], name="concat"
        )  # (2N,1,1)
        x = tf.keras.layers.Flatten()(concat)
        x = tf.keras.layers.Dense(
            64, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(reg)
        )(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dense(3, activation="softmax")(x)
        self.model = tf.keras.Model(inputs=[user, course], outputs=x)
        self.model.compile(
            loss=self.params["loss"],
            optimizer=self.params["optimizer"],
            metrics=self.params["metrics"],
        )

    def fit(self, data):
        logger.debug("Entering fit method of class {} ".format(self.__class__.__name__))
        train, val = train_test_split(
            data, test_size=self.params["test_size"], stratify=data.target
        )
        self.history = self.model.fit(
            x=[train.user, train.course],
            y=train.target,
            validation_data=([val.user, val.course], val.target),
            batch_size=self.params["batch_size"],
            shuffle=True,
            epochs=self.params["epochs"],
            verbose=1,
            callbacks=[cp_callback, tensorboard_callback, train_stop_callback],
        )
        logger.debug(
            "Finished running fit method of class {} ".format(self.__class__.__name__)
        )
        return self

    def predict_similar_users(self, user_handle, num_similar_users=NUM_SIMILAR_USERS):
        try:
            user = self.user_handle_dict[user_handle]
            user_layer = self.model.get_layer("user_embedding")
            user_weights = user_layer.get_weights()[0]
            user_lengths = np.linalg.norm(user_weights, axis=1)
            noramlized_users = (user_weights.T / user_lengths).T
            dists = np.dot(noramlized_users, noramlized_users[user])
            dists = dists[~np.isnan(dists) & ~np.isinf(dists)]
            similar_users = []
            for user_idx, score in enumerate(dists):
                if user_idx != user:
                    similar_users.append((user_idx, score))
            k_neighbors = heapq.nlargest(
                num_similar_users, similar_users, key=lambda t: t[1]
            )
            data = [
                (self.reverse_user_handle_dict[user[0]], user[1])
                for user in k_neighbors
            ]
            logger.debug(f"Predictions for user_handle {user_handle} {data}")
            logger.debug(f"Predicted similar users for {user_handle}")
            return pd.DataFrame(
                data, columns=["similar_users", "course_level_sim_score"]
            )
        except KeyError:
            log_exception()

