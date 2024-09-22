from django.core.exceptions import ValidationError
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import (
    OperationSerializer,
    OperationSerializerInfo,
    OperationSerializerListInfo,
)
from .service import OperationService


class OperationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    @extend_schema(
        summary=("Displays all active operations "),
        responses=OperationSerializerListInfo(many=True),
    )
    def list(self, request):
        operations = OperationService().fetch_active_operations()
        if operations is None:
            return Response(
                {"detail": "There ara problems with fetch operations."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not operations:
            return Response(
                {"detail": "There are no active operations available."},
                status=status.HTTP_200_OK,
            )

        serializer = OperationSerializerListInfo(operations, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary=("Displays one operation by id"),
        responses=OperationSerializerInfo(many=True),
    )
    def retrieve(self, request, pk):
        operation = OperationService.fetch_operation_by_id(pk)
        if operation is None:
            return Response(
                {"detail": "There are no an operation available."},
                status=status.HTTP_200_OK,
            )

        serializer = OperationSerializerInfo(operation)
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
        error_response = self.validate_user_role(request.user)
        if error_response:
            return error_response

        return self.create_operation(request)

    def validate_user_role(self, user):
        """
        Verify that the user has the role of operator.
        If the user has a different role, return a response
        with a 403 status code
        """
        try:
            OperationService.validate_user(user.rol)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    def create_operation(self, request):
        """
        Validate the data sent in the request and create a new operation.
        """
        serializer = OperationSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            new_operation = serializer.save()
            operation_data = OperationSerializer(new_operation).data
            return Response(
                operation_data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
