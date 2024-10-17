from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework import status, generics
from django.contrib.auth import authenticate
from .models import Review, Movie, User
from .serializers import ReviewSerializer, MovieSerializer, SignUpSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView


# signup view for registeration with post funcation to vladatie data and save it into database
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            respone = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=respone, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


# list all views and allow only authenticated users to create new reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # only authenticated users

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)  # set the review to logged in user

  

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # users to edit only their own review
        return serializer.save(user=self.request.user)
    
    
    
    def delete(self, serializer):
        return serializer.delete(
            user=self.request.user
        )  # users to delete only their own review


class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRetrieveView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            # Find the user by email
            user = User.objects.get(email=email)

            # Check the password
            if user.check_password(password):
                response = {"message": "login successful", "token": user.auth_token.key}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={"message": "invalid email or password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                data={"message": "invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
