from django.urls import path

from .views import (
    index,
    MovieListView,
    ReviewListView,
    MovieCreateView,
    ReviewCreateView,
)


urlpatterns = [
    path("", index, name="index"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("reviews/", ReviewListView.as_view(), name="review_list"),
    path("movies/create/", MovieCreateView.as_view(), name="movie_create"),
    path("reviews/create/", ReviewCreateView.as_view(), name="review_create"),
]

app_name = "movie_review"
