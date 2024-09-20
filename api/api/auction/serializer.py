from rest_framework import serializers

from api.auction.models import Auction, Offert
from api.operation.models import Operation

from .repository.auction_repository import AuctionRepository


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


class OffertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offert
        fields = "__all__"


class OffertSerializerCreate(serializers.ModelSerializer):
    operation_id = serializers.CharField()

    class Meta:
        model = Offert
        fields = ["amount", "rate_wished", "operation_id"]

    def validate(self, data):
        """
        Valida los datos de la oferta antes de crearla.
        """
        # Extract the request and the user from the context
        request = self.context.get("request")
        request_user = request.user

        # Relate the operation to the auction
        auction = AuctionRepository.get_auction_by_operation_id(
            data["operation_id"]
        )

        # Validate Zone (user role, amount, rate wished)
        self._validate_user_role(request_user)
        self._validate_amount(data["amount"], auction.remaining_amount)
        self._validate_rate_wished(
            data["rate_wished"], auction.operation.anual_rate
        )

        return data

    def _validate_user_role(self, user):
        """
        Valida que el rol del usuario sea 'investor'.
        """
        if user.rol != "investor":
            raise serializers.ValidationError(
                f"The role '{user.rol}' cannot create an offer."
            )

    def _validate_amount(self, amount, remaining_amount):
        """
        Valida que el monto de la oferta sea mayor a cero y menor al monto restante de la subasta.
        """
        if amount <= 0 or amount > remaining_amount:
            raise serializers.ValidationError(
                f"The amount must be greater than zero and lower than the remaining amount of {remaining_amount}."
            )

    def _validate_rate_wished(self, rate_wished, max_rate):
        """
        Valida que la tasa deseada sea mayor a cero y menor o igual a la tasa anual máxima de la operación.
        """
        if rate_wished <= 0 or rate_wished > max_rate:
            raise serializers.ValidationError(
                f"The rate wished must be greater than zero and lower than or equal to the anual rate of {max_rate}."
            )


class AuctionDetailSerializer(serializers.ModelSerializer):
    operation = OperationSerializer(read_only=True)

    offers = OffertSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = ["id", "remaining_amount", "operation", "offers"]
