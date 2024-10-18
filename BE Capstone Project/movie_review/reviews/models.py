from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds unique email field.
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        # it shows the username instead of the default user ID.
        return self.username


# Movie model to store movie details.
class Movie(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    release_date = models.DateTimeField()
    genre = models.CharField(max_length=50)


class Review(models.Model):
    """
    Review model to store user reviews for movies.
    Each review is linked to a movie and a user.
    """
    class Rating(models.IntegerChoices):
        """
        Defines the rating system for reviews using Django's IntegerChoices.
        Maps integers to human-readable values (e.g., "1 star").
        """
        ONE = 1, "1 star"
        TWO = 2, "2 stars"
        THREE = 3, "3 stars"
        FOUR = 4, "4 stars"
        FIVE = 5, " 5 stars"

    rating = models.IntegerField(choices=Rating.choices, blank=False)
    review_content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    create_date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
