from flask_restful import Resource, reqparse
from db_model import UserListModel


class SimilarUserList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_handle", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("model_handle", type=str, required=False)

    def post(self):
        data = SimilarUserList.parser.parse_args()
        try:
            user_handle = data["user_handle"]
            if data["model_handle"]:
                model_handle = data["model_handle"]
                response = UserListModel.query(
                    user_handle, UserListModel.model_handle == model_handle.lower()
                ).__next__()
            else:
                response = UserListModel.query(user_handle).__next__()
            return (
                {
                    "model_handle": response.model_handle,
                    "similar_users": response.similar_users,
                },
            )
        except StopIteration:
            return (
                {"message": f'User with user_handle: {data["user_handle"]} not found'},
                404,
            )

