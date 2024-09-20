import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import OperationFactory, UserCustomFactory

register(UserCustomFactory)
register(OperationFactory)


@pytest.fixture
def api_client():
    return APIClient()
