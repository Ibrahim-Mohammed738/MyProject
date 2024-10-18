from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework import status, generics, filters
from django.contrib.auth import authenticate
from .models import Review, Movie, User
from .serializers import ReviewSerializer, MovieSerializer, SignUpSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class SignUpView(generics.GenericAPIView):
    """
    signup view for registeration with post funcation to vladatie data
    and save it into database.
    any user can access this view without authentication.
    """

    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        """
        Handle POST requests to register a new user.
        Validates the input and saves the user if valid.
        """
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            # Save the new user and return success message
            serializer.save()
            respone = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=respone, status=status.HTTP_201_CREATED)
        # If validation fails, return errors
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Lists all reviews and allows authenticated users to create new reviews.
    Supports filtering by rating and creation date, and searching by movie title.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # only authenticated users
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["rating", "create_date"]
    search_fields = ["movie__title"]

    def get_serializer_context(self):
        """
        Passes the request context to the serializer.
        This allows the serializer to access the request.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    # Handles POST requests to create a new review.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows retrieving, updating, or deleting a specific review.
    Only the owner of the review can modify or delete it.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # only the owner of the review can update it
    def perform_update(self, serializer):
        if serializer.instance.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this review.")

    # only the owner of the review can delete it
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this review.")


class MovieListCreateView(generics.ListCreateAPIView):
    """
    Lists all movies and allows authenticated users to create new movies.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


class MovieRetrieveView(generics.RetrieveAPIView):
    """
    Retrieves the details of a specific movie.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class LoginView(APIView):
    """
    Handles user login by checking the email and password.
    If valid, returns an authentication token for the user.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            # Find the user by email
            user = User.objects.get(email=email)

            # Check the password
            if user.check_password(password):
                # Return the authentication token if login is successful
                response = {"message": "login successful", "token": user.auth_token.key}
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                # Return an error if the password is incorrect
                return Response(
                    data={"message": "invalid email or password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            # Return an error if the user does not exist
            return Response(
                data={"message": "invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
