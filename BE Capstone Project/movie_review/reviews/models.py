from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


# Movie model to store movie details.
class Movie(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    release_date = models.DateTimeField()
    genre = models.CharField(max_length=50)


class Review(models.Model):
    # rating class to limit the choices from 1 to 5
    class Rating(models.IntegerChoices):
        ONE = 1, "1 star"
        TWO = 2, "2 stars"
        THREE = 3, "3 stars"
        FOUR = 4, "4 stars"
        FIVE = 5, " 5 stars"

    rating = models.IntegerField(choices=Rating.choices, blank=False)
    # movie_title = models.CharField(max_length=150, null=False, blank=False)
    review_content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    create_date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
