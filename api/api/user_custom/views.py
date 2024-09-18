from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserCustomSerializer


class UserCustomViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        users = UserCustomSerializer.get_all()
        serializer = UserCustomSerializer(users, many=True)
        return Response(serializer.data)

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

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = UserCustomSerializer.user_auth(username, password)
        if user is not None:
            token = Token.objects.create(user=user)
            serializer = UserCustomSerializer(user)

            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
