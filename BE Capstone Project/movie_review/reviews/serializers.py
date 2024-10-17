from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import Review, Movie, User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        # ensure the email is uniqe and isnt used again.
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("This email already exists")

        username_exists = User.objects.filter(username=attrs["username"]).exists()
        if username_exists:
            raise ValidationError("This username is already taken")

        return attrs

    def create(self, validated_data):
        # Hash the password before saving
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )

        # Create a token for the newly created user
        Token.objects.create(user=user)

        return user


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username", read_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    movie_name = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "movie_title",
            "movie_name",
            "review_content",
            "create_date",
            "user",
        ]

    # Custom validation to ensure the rating is between 1 and 5
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_movie_title(self, value):
        if not Movie.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                f"'{value}' is not listed in the movie database!"
            )
        return value

    def create(self, validated_data):
        movie_name = validated_data.pop("movie_name")
        movie = Movie.objects.get(title__iexact=movie_name)
        user = self.context["request"].user
        return Review.objects.create(movie=movie, user=user, **validated_data)


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "release_date", "genre", "reviews"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
