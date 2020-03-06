from flask import Flask
from flask_restful import Api
from server.resources import SimilarUserList
from db_utils import create_table
from DEFAULTS import SERVER_PORT

app = Flask(__name__)
api = Api(app)
api.add_resource(SimilarUserList, "/similar-users/")

if __name__ == "__main__":
    create_table()
    app.run(port=SERVER_PORT, debug=True)
