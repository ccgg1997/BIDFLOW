from api.user_custom.models import UserCustom


class UserCustomRepository:

    @staticmethod
    def create_user(username, dni, rol, email, password):
        user = UserCustom(username=username, dni=dni, rol=rol, email=email)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_all():
        return UserCustom.objects.all()

    @staticmethod
    def get_by_username(username):
        try:
            return UserCustom.objects.get(username=username)
        except UserCustom.DoesNotExist:
            return None
