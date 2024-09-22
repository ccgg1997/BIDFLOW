from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .repository.auction_repository import AuctionRepository
from .serializer import (
    AuctionDetailSerializer,
    OffertSerializer,
    OffertSerializerCreate,
)


class AuctionViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar las subastas (Auctions).
    """

    def get_permissions(self):
        return [IsAuthenticated()]

    @extend_schema(
        summary=("Displays one operation by id"),
        responses=AuctionDetailSerializer(),
    )
    def retrieve(self, request, pk):
        """
        List all the auctions for a specific operation.
        """

        try:
            auction = AuctionRepository.get_auction_by_operation_id(pk)
            serializer = AuctionDetailSerializer(auction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {
                    "error": "Auction not found for the specified operation."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Create an offert for an auction (only investors)",
        request=OffertSerializerCreate,
        responses={
            201: OffertSerializer,
            400: "Error en los datos enviados",
        },
    )
    def create(self, request):
        """
        Crear una oferta basada en los datos del request.
        """
        user_id = request.user.id

        # Validate the data sent by the user
        serializer = OffertSerializerCreate(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Create the offert
        created_offert = AuctionRepository.create_offert(
            serializer.validated_data["amount"],
            serializer.validated_data["rate_wished"],
            user_id,
            serializer.validated_data["operation_id"],
        )

        if created_offert is None:
            return self.error_response("Can't create an offert.")

        return self.success_response(created_offert)

    @action(detail=False, methods=["get"])
    def ask_mistral(self, request):
        """analize the higest 10 operations active. Analize the amount, the
        anual rate and the amount of operations of by user. it return
        the 3 best operation to the user

        Returns:
            Recommend 3 operations for the user (str)
        """
        return Response(
            {AuctionRepository.ask_mistral()},
            status=status.HTTP_200_OK,
        )

    # Aux methods
    def success_response(self, offert):
        """
        Responder con la oferta creada y el estado HTTP 201.
        """
        serialized_offert = OffertSerializer(offert)
        return Response(
            {"detail": serialized_offert.data},
            status=status.HTTP_201_CREATED,
        )

    # Aux methods
    def error_response(self, message):
        """
        Responder con un mensaje de error y el estado HTTP 400.
        """
        return Response(
            {"error": message},
            status=status.HTTP_400_BAD_REQUEST,
        )
