import pandas as pd
from .data_utils import make_lower_case, remove_duplicates
from paths import interests_file, user_course_views_file
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

class UserCourseViewTimeDataProcessor:

    def load_data():
        try: 
            raw_data=pd.read_csv(user_course_views_file)
            cleaned_data=raw_data.copy()
            cleaned_data=cleaned_data.groupby(['user_handle', 'course_id']).agg({'view_time_seconds':'sum'}).reset_index()
            cleaned_data=cleaned_data[cleaned_data.view_time_seconds>0]
            assert cleaned_data.isnull().sum().any()==0
            return cleaned_data

        except FileNotFoundError:
            log_exception()

        except KeyError:
            log_exception()