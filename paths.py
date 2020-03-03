import os.path
from datetime import datetime
import dotenv
from pathlib import Path
current_time=datetime.now().strftime("%Y%m%d-%H%M%S")
project_dir = Path(__file__).resolve().parents[0]
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)
data_dir = os.path.join(project_dir, "data")
raw_data_dir=os.path.join(data_dir, "raw")
models_dir = os.path.join(project_dir, "models")
notebooks_dir = os.path.join(project_dir, "notebooks")
course_tags_file = os.path.join(raw_data_dir, "course_tags.csv")
user_assessment_scores_file = os.path.join(raw_data_dir, "user_assessment_scores.csv")
user_course_views_file = os.path.join(raw_data_dir, "user_course_views.csv")
interests_file = os.path.join(raw_data_dir, "user_interests.csv")
generator_log_file = os.path.join(project_dir, f"generator_{current_time}.log")