from flask import Flask
from flask_restful import Api
from resources import SimilarUserList

app = Flask(__name__)
app.config.from_object('server_config.DevelopmentConfig')
api=Api(app)
api.add_resource(SimilarUserList,'/similar-users/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        with app.app_context():
            db.create_all()
    app.run(port=5000)