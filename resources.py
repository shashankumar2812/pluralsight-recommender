from flask_restful import Resource, reqparse
from db_model import UserListModel

class SimilarUserList(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument(
        'user_handle',
        type=int,
        required=True,
        help='This field cannot be left blank!'
    )

    def post(self):
        data=SimilarUserList.parser.parse_args()
        try: 
            request_data=data['user_handle']
            response=UserListModel.query(request_data).__next__()
            return {'request_data': request_data, 'data': {'similar_users': response.similar_users}}
        except StopIteration:
            return {'message': f'User with user_handle: {data["user_handle"]} not found'}, 404