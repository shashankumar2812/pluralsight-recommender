from uuid import uuid4
from flask import Flask
from flask_dynamo import Dynamo
import pytest
from db_model import UserListModel
from test_utils import random_with_N_digits, make_table



@pytest.fixture
def app():
    app = Flask(__name__)
    prefix = uuid4().hex
    app.config['DEBUG'] = True
    app.config['DYNAMO_TABLES'] = [
        make_table('%s-phones' % prefix, 'number', 'N'),
        make_table('%s-users' % prefix, 'username', 'S'),
    ]
    return app

@pytest.fixture
def dynamo(app):
    dynamo = Dynamo(app)
    return dynamo

@pytest.fixture
def local_app(app):
    app.config['DYNAMO_ENABLE_LOCAL'] = True
    return app

@pytest.fixture
def create_mock_user_entry_in_db(get_mock_user_sim_users_pair):
    user, sim_users=get_mock_user_sim_users_pair
    user = UserListModel(user_handle=user, similar_users=sim_users)
    print()
    user.save()

@pytest.fixture
def get_mock_user_sim_users_pair(get_mock_user, get_mock_sim_user_list):
    return get_mock_user, get_mock_sim_user_list

@pytest.fixture
def get_mock_user():
    return random_with_N_digits(10)

@pytest.fixture
def get_mock_sim_user_list():
    return [random_with_N_digits(10) for i in range(6)]