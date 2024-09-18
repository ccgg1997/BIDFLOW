import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    login_endpoint = "/api/user/login/"

    def test_user_login_missing_fields(self, api_client):
        # Act
        response = api_client.post(
            self.login_endpoint,
            data={},
            format="json",
        )

        assert response.status_code == 400
        assert "username" in response.data
        assert "password" in response.data
