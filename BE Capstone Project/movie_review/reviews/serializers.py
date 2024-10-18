from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import Review, Movie, User


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user sign-up (registration).
    Converts user data into a User model instance and validates
    the uniqueness of email and username.
    """

    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        # check if email is unique
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("This email already exists")

        # Check if username is unique
        username_exists = User.objects.filter(username=attrs["username"]).exists()
        if username_exists:
            raise ValidationError("This username is already taken")

        return attrs  # If valid, returns the attributes for further processing

    def create(self, validated_data):
        # Create a new user with hashed password
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )

        # Create an authentication token for the new user
        Token.objects.create(user=user)

        return user


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for handling review creation and displaying reviews.
    It links reviews with users and movies.
    """

    user = serializers.CharField(source="user.username", read_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    movie_name = serializers.CharField(write_only=True)  # For input only, not output

    class Meta:
        model = Review
        fields = [
            "id",  # The review ID
            "rating",  # The rating given in the review
            "movie_title",  # Movie title (read-only, comes from the movie model)
            "movie_name",  # Movie name used for submitting a review (write-only)
            "review_content",  # Text content of the review
            "create_date",  # Date the review was created
            "user",  # Username of the review creator (read-only)
        ]

    # Validates that the rating is between 1 and 5
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_movie_title(self, value):
        # Check if the movie exists in the database
        if not Movie.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                f"'{value}' is not listed in the movie database!"
            )
        return value

    def create(self, validated_data):
        # create a new reveiw
        movie_name = validated_data.pop("movie_name")  # Remove movie_name from the validated data
        movie = Movie.objects.get(title__iexact=movie_name)  # Find the movie by its name
        user = self.context["request"].user  # Get the current authenticated user
        return Review.objects.create(movie=movie, user=user, **validated_data)  # Create a new review



class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying movie details.
    It includes the list of associated reviews.
    """
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "release_date", "genre", "reviews"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"] # Only username and email are returned
