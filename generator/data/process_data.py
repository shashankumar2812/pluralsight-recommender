import pandas as pd
from .data_utils import make_lower_case, remove_duplicates
from paths import interests_file
from helpers.utils import log_exception

class UserInterestDataProcessor:

    def load_data():
        try: 
            raw_data=pd.read_csv(interests_file)
            cleaned_data=raw_data.copy()
            cleaned_data['interest_tag']=cleaned_data['interest_tag'].apply(make_lower_case)
            cleaned_data=cleaned_data.groupby(['user_handle'])['interest_tag'].apply(lambda x: ','.join(x)).reset_index()
            cleaned_data['interest_tag']=cleaned_data['interest_tag'].apply(remove_duplicates)
            assert cleaned_data.isnull().sum().any()==0
            return cleaned_data

        except FileNotFoundError:
            log_exception()

        except KeyError:
            log_exception()