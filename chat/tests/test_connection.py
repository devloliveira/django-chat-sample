import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.auth import login

from chat.models import UserConnection


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class Test__connections:
    def test__request_connection(self, client):

        # Setup
        userA = User.objects.create_user('userA', 'userA', 'dummy-password')
        userB = User.objects.create_user('userB', 'userB', 'dummy-password')

        login_response = client.post(f'/login/', {'username': 'userA', 'password': 'dummy-password'})
        assert login_response.status_code == 200

        # Creates a connection request between both users
        response = client.post(f'/chat/connection/request/{userB.id}')
        assert response.status_code == 200

        conn = UserConnection.get_connection(userA, userB)
        assert conn is not None
        assert conn.status == 'p'

        # A second attempt should not be allowed
        response = client.post(f'/chat/connection/request/{userB.id}')
        assert response.status_code == 409

    def test__accept_connection(self, client):

        # Setup
        userA = User.objects.create_user('userA', 'userA', 'dummy-password')
        userB = User.objects.create_user('userB', 'userB', 'dummy-password')

        UserConnection.objects.create(author=userA, target_user=userB)

        login_response = client.post(f'/login/', {'username': 'userB', 'password': 'dummy-password'})
        assert login_response.status_code == 200

        # Accepts
        response = client.post(f'/chat/connection/accept/{userA.id}')
        assert response.status_code == 200
        conn = UserConnection.get_connection(userA, userB)
        assert conn is not None
        assert conn.status == 'a'

    def test__reject_connection(self, client):

        # Setup
        userA = User.objects.create_user('userA', 'userA', 'dummy-password')
        userB = User.objects.create_user('userB', 'userB', 'dummy-password')

        UserConnection.objects.create(author=userA, target_user=userB)

        login_response = client.post(f'/login/', {'username': 'userB', 'password': 'dummy-password'})
        assert login_response.status_code == 200

        # Accepts
        response = client.post(f'/chat/connection/reject/{userA.id}')
        assert response.status_code == 200
        conn = UserConnection.get_connection(userA, userB)
        assert conn is not None
        assert conn.status == 'r'
