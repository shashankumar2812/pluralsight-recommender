from datetime import datetime
import logging
from db_model import UserListModel
from helpers.utils import log_exception

logger = logging.getLogger(__name__)


def run_similar_user_generator(gen_model, params, data_loader, model_handle):
    logger.info("Entering run_similar_user_generator function")
    try:
        model = gen_model(**params)
        data = data_loader.load_data()
        model.fit(data)
        count = 0
        for user_handle in data.user_handle.unique():
            count += 1
            similar_users = model.predict_similar_users(
                user_handle=user_handle
            ).similar_users.tolist()
            user = UserListModel(
                user_handle=int(user_handle),
                model_handle=model_handle,
                similar_users=similar_users,
                created_at=datetime.utcnow(),
            )
            user.save()
            if count % 1000 == 0:
                logger.info(f"Saved {count} records in the Database")
        logger.info("Existing run_similar_user_generator function")
    except:
        log_exception()
