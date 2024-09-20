from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import OperationSerializer


class OperationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    @extend_schema(
        summary=("Displays all active operations "),
        responses=OperationSerializer(many=True),
    )
    def list(self, request):

        operations = OperationSerializer.fetch_active_operation()
        if not operations:
            return Response(
                {"detail": "There are no active operations available."},
                status=status.HTTP_200_OK,
            )

        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary=("Displays one operation by id"),
        responses=OperationSerializer(many=True),
    )
    def retrieve(self, request, pk):

        operation = OperationSerializer.fetch_operation_id(pk)
        if operation is None:
            return Response(
                {"detail": "There are no an operation available."},
                status=status.HTTP_200_OK,
            )

        serializer = OperationSerializer(operation)
        return Response(serializer.data)

    @extend_schema(
        summary="Registers an investment operation with"
        "a minimum of 1 day in advance. The amount"
        "must be positive, and the topic should "
        "describe the investment. Specify the"
        " annual interest rate (EA) and the"
        " investment deadline.",
        request=OperationSerializer,
        responses={
            201: OperationSerializer,
            400: "Error en los datos enviados",
        },
    )
    def create(self, request):
        request.data["user"] = request.user.id
        serializer = OperationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_operation = serializer.save()
            operation_data = OperationSerializer(new_operation).data

            return Response(
                operation_data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
