from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import OperationSerializer


class OperationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    @extend_schema(
        summary="Lista todas las operaciones activas",
        responses=OperationSerializer(many=True),
    )
    def list(self, request):
        operations = OperationSerializer.fetch_active_operation()
        if not operations:
            return Response(
                {"detail": "No hay operaciones activas disponibles."},
                status=status.HTTP_200_OK,
            )

        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Registro Operación",
        request=OperationSerializer,
        responses={
            201: OperationSerializer,
            400: "Error en los datos enviados",
        },
    )
    def create(self, request):
        request.data["user"] = request.user.id
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            new_operation = serializer.save()
            operation_data = OperationSerializer(new_operation).data

            return Response(
                {
                    "operation": operation_data,
                    "status": "Operation success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        user_name = request.data["username"]
        operation_id = request.data["operation_id"]
