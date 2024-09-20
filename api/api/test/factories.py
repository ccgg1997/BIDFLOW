import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from api.operation.models import Operation
from api.user_custom.models import UserCustom


class UserCustomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserCustom
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(
        lambda: make_password("password123")
    )
    dni = "0.2"
    rol = "operator"


class OperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Operation
        django_get_or_create = ("topic",)

    amount = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    topic = factory.Faker("word")
    description = factory.Faker("sentence")
    anual_rate = 0.7
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=4)
    )
    user = factory.SubFactory(UserCustomFactory)
    status = True
