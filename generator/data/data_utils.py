from surprise import Dataset, KNNBasic, Reader


def split_with_comma(word):
    return word.split(",")


def make_lower_case(word):
    if word:
        return word.lower()


def remove_duplicates(words):
    unique_word_list = list(set(words.split(",")))
    return ",".join(unique_word_list)


def create_user_indices_from_user_handle(data):
    user_idx_dict = {}
    for idx, user in enumerate(data.user_handle.unique()):
        if user not in user_idx_dict:
            user_idx_dict[user] = idx
    return user_idx_dict


def create_course_indices_from_course_id(data):
    course_idx_dict = {}
    for idx, course in enumerate(data.course_id.unique()):
        if course not in course_idx_dict:
            course_idx_dict[course] = idx
    return course_idx_dict


def create_surprise_data_set(df, target_col):
    reader = Reader(rating_scale=(-df[target_col].min(), df[target_col].max()))
    data = Dataset.load_from_df(df, reader)
    surprise_data_set = data.build_full_trainset()
    return surprise_data_set

def _download_raw_data(dest_path):
    """
    Download the dataset.
    """

    url = 'https:s3//ml.personal.com/pluralsight_ml_eng_data_files.tar.gz'
    req = requests.get(url, stream=True)

    print('Downloading raw data')

    with open(dest_path, 'wb') as fd:
        for chunk in req.iter_content():
            fd.write(chunk)
