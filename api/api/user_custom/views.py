from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, UserCustomSerializer


class UserCustomViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="Lista todos los usuarios", responses=UserCustomSerializer(many=True)
    )
    def list(self, request):
        users = UserCustomSerializer.get_all()
        serializer = UserCustomSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Registro de nuevo usuario",
        request=UserCustomSerializer,
        responses={201: UserCustomSerializer, 400: "Error en los datos enviados"},
    )
    def create(self, request):
        serializer = UserCustomSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)

            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Inicio de sesión",
        description="Permite a un usuario iniciar sesión y obtener un token de autenticación.",
        request=LoginSerializer,  # Ahora usas el nuevo serializer de login
        responses={
            200: UserCustomSerializer,
            400: "Credenciales inválidas",
        },
    )
    @action(detail=False, methods=["post"])
    def login(self, request):

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = UserCustomSerializer.user_auth(username, password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserCustomSerializer(user)

        return Response(
            {
                "token": token.key,
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
