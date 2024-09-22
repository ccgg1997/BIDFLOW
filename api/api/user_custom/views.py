from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, UserCustomSerializer
from .service import UserCustomService


class UserCustomViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="Create new user. IMPORTANT ROLE FIELD (INVESTOR OR OPERATOR)",
        request=UserCustomSerializer,
        responses={
            201: UserCustomSerializer,
            400: "Error in the submitted data",
        },
    )
    def create(self, request):
        serializer = UserCustomSerializer(data=request.data)
        if serializer.is_valid():
            user = UserCustomService.create_user(
                serializer.validated_data
            )
            token = Token.objects.create(user=user)

            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="User Login",
        description=(
            "Allows a user to log in and obtain an authentication token."
        ),
        request=LoginSerializer,
        responses={
            200: UserCustomSerializer,
            400: OpenApiResponse(
                description="Error in the submitted data"
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def login(self, request):

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = UserCustomService.authenticate_user(username, password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserCustomSerializer(user)

        return Response(
            {
                "token": token.key,
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
