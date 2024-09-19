import pytest
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    endpoint = "/api/user/"

    def test_user_get(self, user_custom_factory, api_client):
        user = user_custom_factory()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = api_client.get(self.endpoint)
        assert response.status_code == 200

    def test_user_get_without_token(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == 401

    def test_user_create(self, api_client):
        response = api_client.post(
            self.endpoint,
            data={
                "username": "camilo",
                "dni": "string",
                "rol": "inversor",
                "email": "user@example.com",
                "password": "camilo",
            },
            format="json",
        )
        assert response.status_code == 201

    def test_user_create_missing_Data(self, api_client):
        response = api_client.post(
            self.endpoint,
            data={
                "username": "camilo",
                "dni": "string",
                "email": "user@example.com",
            },
            format="json",
        )
        assert response.status_code == 400
