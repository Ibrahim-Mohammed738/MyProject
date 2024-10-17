from django.urls import path
from .views import (
    ReviewDetailView,
    ReviewListCreateView,
    MovieListCreateView,
    MovieRetrieveView,
    SignUpView,
    LoginView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="sign_up"),
    path("login/", LoginView.as_view(), name="login"),
    path("reviews-list/", ReviewListCreateView.as_view(), name="review-list"),
    path("reviews-detail/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
    path("movie-list/", MovieListCreateView.as_view(), name="movie-list"),
    path("movie-detail/<int:pk>/", MovieRetrieveView.as_view(), name="movie-detail"),
]
