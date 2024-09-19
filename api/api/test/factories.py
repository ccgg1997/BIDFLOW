import factory
from django.contrib.auth.hashers import make_password

from api.user_custom.models import UserCustom


class UserCustomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserCustom
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("password123"))
    dni = factory.Faker("random_number", digits=8, fix_len=True)
    rol = "inversor"
