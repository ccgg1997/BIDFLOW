import pytest
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


class TestOperationEndpoints:
    endpoint = "/api/operation/"

    def test_operation_list(
        self, operation_factory, api_client, user_custom_factory
    ):
        user = user_custom_factory(rol="operator")
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        operation_factory.create_batch(3, user=user)

        response = api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_operation_list_without_token(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == 401

    def test_operation_retrieve(
        self, operation_factory, api_client, user_custom_factory
    ):
        user = user_custom_factory()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        operation = operation_factory(user=user, anual_rate=20)

        response = api_client.get(f"{self.endpoint}{operation.id}/")

        assert response.status_code == 200
        assert response.data["id"] == operation.id
        assert response.data["amount"] == str(operation.amount)

    def test_operation_create(self, api_client, user_custom_factory):
        user = user_custom_factory(rol="operator")
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        operation_data = {
            "amount": "5000",
            "topic": "Real",
            "description": "Investment opportunity in real estate sector.",
            "anual_rate": "0.5",
            "end_date": "2024-10-22",
        }

        response = api_client.post(
            "/api/operation/",
            data=operation_data,
            format="json",
        )

        assert response.status_code == 201
        assert response.data["amount"] == "5000.00"
        assert response.data["topic"] == "Real"

    def test_operation_create_missing_data(
        self, api_client, user_custom_factory
    ):
        user = user_custom_factory()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        operation_data = {
            "topic": "Missing Data",
            "description": "This test should fail due to missing data.",
            "anual_rate": "0.4",
            "start_date": "2024-09-20",
            "user": user.id,
            "status": True,
        }

        response = api_client.post(
            self.endpoint,
            data=operation_data,
            format="json",
        )

        assert response.status_code == 400
