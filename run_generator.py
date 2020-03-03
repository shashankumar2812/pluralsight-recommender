from datetime import datetime
import logging
from db_model import UserListModel
from DEFAULTS import GEN_LOG_LEVEL
from generator.data.data_utils import split_with_comma
from generator.data.process_data import UserInterestDataProcessor
from generator.models.similar_interest_model import SimilarInterestUserModel
from helpers.utils import log_exception
from paths import generator_log_file

logger = logging.getLogger(__name__)

class SimilarUserGenerator:
    def run():
        logger.info('Entering run method of Class {} '.format(__class__.__name__))
        try: 
            params=dict(analyzer=split_with_comma, min_df=5)  
            sm=SimilarInterestUserModel(params=params)
            data=UserInterestDataProcessor.load_data()
            sm.fit(data)
            count=0
            for user in data.user_handle.unique():
                count+=1
                similar_users=sm.predict_simiar_users(user_handle=user).similar_users.tolist()
                user = UserListModel(user_handle=int(user), similar_users=similar_users)
                user.save()
                if count%1000==0:
                    logger.info(f'Saved {count} records in the Database')
            logger.info('Finished run method of Class {} '.format(__class__.__name__))
        except:
            log_exception()

def main():
    start_time = datetime.now()
    logger.info('Starting Iris!')
    SimilarUserGenerator.run()
    logger.info("Iris Done Generating Similar Users!")
    logger.info("Time of running the script: {}".format(datetime.now() - start_time))



if __name__ == '__main__':
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[logging.FileHandler(generator_log_file, mode='w'),
                                  logging.StreamHandler()],

                        level=GEN_LOG_LEVEL)
    main()