from api.user_custom.repository.user_custom_repository import UserCustomRepository


class UserCustomFactory:
    @staticmethod
    def create_inversor(username, dni, email, password):
        return UserCustomRepository().create_user(
            username, dni, "inversor", email, password
        )

    @staticmethod
    def create_operador(username, dni, email, password):
        return UserCustomRepository().create_user(
            username, dni, "operador", email, password
        )
