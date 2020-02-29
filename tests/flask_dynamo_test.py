from flask_dynamo import Dynamo
import pytest

@pytest.yield_fixture
def active_dynamo(dynamo, app):
    with app.app_context():
        try:
            dynamo.create_all(wait=True)
            yield dynamo
        finally:
            try:
                dynamo.destroy_all()
            except Exception as e:
                print(f'Unable to clean up: {e}')

def test_dynamodb_table_access(active_dynamo, app):
    with app.app_context():
        assert len(active_dynamo.tables.keys()) == 2
        for table_name, table in active_dynamo.tables.items():
            assert active_dynamo.tables[table_name].name == table_name

def test_valid_dynamodb_local_settings(local_app):
    local_app.config['DYNAMO_LOCAL_PORT'] = 8000
    local_app.config['DYNAMO_LOCAL_HOST'] = 'localhost'
    Dynamo(local_app)