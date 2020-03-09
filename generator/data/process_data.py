from amazon import read_file_from_s3
from .data_utils import make_lower_case, remove_duplicates
from paths import interests_file, user_course_views_file
from helpers.utils import log_exception


class UserInterestDataProcessor:
    def load_data():
        try:
            raw_data = read_file_from_s3(interests_file)
            cleaned_data = raw_data.copy()
            cleaned_data["interest_tag"] = cleaned_data["interest_tag"].apply(
                make_lower_case
            )
            cleaned_data = (
                cleaned_data.groupby(["user_handle"])["interest_tag"]
                .apply(lambda x: ",".join(x))
                .reset_index()
            )
            cleaned_data["interest_tag"] = cleaned_data["interest_tag"].apply(
                remove_duplicates
            )
            assert cleaned_data.isnull().sum().any() == 0
            return cleaned_data

        except FileNotFoundError:
            log_exception()

        except KeyError:
            log_exception()


class UserCourseViewTimeDataProcessor:
    def load_data():
        try:
            raw_data = read_file_from_s3(user_course_views_file)
            cleaned_data = raw_data.copy()
            cleaned_data = (
                cleaned_data.groupby(["user_handle", "course_id"])
                .agg({"view_time_seconds": "sum"})
                .reset_index()
            )
            cleaned_data = cleaned_data[cleaned_data.view_time_seconds > 0]
            assert cleaned_data.isnull().sum().any() == 0
            return cleaned_data

        except FileNotFoundError:
            log_exception()

        except KeyError:
            log_exception()


class UserCourseLevelDataProcessor:
    def load_data():
        try:
            raw_data = read_file_from_s3(user_course_views_file)
            cleaned_data = raw_data.copy()
            user_idx_dict = {}
            course_idx_dict = {}
            for idx, user in enumerate(raw_data.user_handle.unique()):
                if user not in user_idx_dict:
                    user_idx_dict[user] = idx
            for idx, course in enumerate(raw_data.course_id.unique()):
                if course not in course_idx_dict:
                    course_idx_dict[course] = idx
            course_level_dict = dict(zip(raw_data.course_id, raw_data.level))
            cleaned_data["user"] = cleaned_data["user_handle"].map(user_idx_dict)
            cleaned_data["course"] = cleaned_data["course_id"].map(course_idx_dict)
            cleaned_data = cleaned_data[cleaned_data.view_time_seconds > 0]
            cleaned_data["level"] = cleaned_data["course_id"].map(course_level_dict)
            cleaned_data.drop_duplicates(keep="first", inplace=True)
            target_map_dict = {"Advanced": 2, "Intermediate": 1, "Beginner": 0}
            cleaned_data["target"] = cleaned_data["level"].map(target_map_dict)
            assert cleaned_data.isnull().sum().any() == 0
            return cleaned_data[
                ["user_handle", "user", "course_id", "course", "target"]
            ]

        except FileNotFoundError:
            log_exception()

        except KeyError:
            log_exception()
