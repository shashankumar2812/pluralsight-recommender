import pytest
import requests
from test_utils import random_with_N_digits

URL = 'http://127.0.0.1:5000'  
SIMILAR_USER_ENDPOINT = URL+'/similar-users/' 

def test_similar_users_endpoint_200(get_mock_user, create_mock_user_entry_in_db):
    request_data={'user_handle': get_mock_user}
    r = requests.post(SIMILAR_USER_ENDPOINT, json=request_data)
    print(f'response: {r.json()}')
    assert r.status_code == 200

def test_similar_users_endpoint_404(get_mock_user):
    request_data={'user_handle': get_mock_user}
    print(f'request_data: {request_data}')
    r = requests.post(SIMILAR_USER_ENDPOINT, json=request_data)
    print(f'response: {r}')
    assert r.status_code == 404