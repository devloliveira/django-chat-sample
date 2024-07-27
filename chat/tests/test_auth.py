import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.auth import login


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class Test__auth:

    def test_users_should_be_able_to_login(self, client):
        # Setup
        user = User.objects.create_user('dummy-username', 'dummy-username', 'dummy-password')

        # Act
        response = client.post(f'/login/', {'username': 'dummy-username', 'password': 'dummy-password'})

        # Assert
        assert response.status_code == 200

    def test_incorrect_credentials_should_fail_login(self, client):
        # Setup
        user = User.objects.create_user('dummy-username', 'a@a.com', 'dummy-password')

        # Act
        response = client.post(f'/login/', {'username': 'incorrect-username', 'password': 'incorrect-password'})

        # Assert
        assert response.status_code == 401
