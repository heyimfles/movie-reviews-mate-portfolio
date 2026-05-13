from django.urls import path

from .views import (
    index,
    MovieListView,
    ReviewListView,
    MovieCreateView,
    ReviewCreateView,
    MovieDetailView,
    MovieUpdateView,
    MovieDeleteView,
    ReviewDetailView, ReviewDeleteView, ReviewUpdateView, ViewerDetailView, ViewerUpdateView,
)

from django.contrib.auth import views as auth_views
from movie_review_app.forms import CustomLoginForm


urlpatterns = [
    path(
        "",
        index,
        name="index"
    ),
    path(
        "movies/",
        MovieListView.as_view(),
        name="movie_list"
    ),
    path(
        "reviews/",
        ReviewListView.as_view(),
        name="review_list"
    ),
    path(
        "movies/create/",
        MovieCreateView.as_view(),
        name="movie_create"
    ),
    path(
        "reviews/create/",
        ReviewCreateView.as_view(),
        name="review_create"
    ),
    path(
        "movies/<int:pk>/",
        MovieDetailView.as_view(),
        name="movie_detail"
    ),
    path(
        "movies/<int:pk>/update/",
        MovieUpdateView.as_view(),
        name="movie_update"
    ),
    path(
        "movies/<int:pk>/delete/",
        MovieDeleteView.as_view(),
        name="movie_delete"
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review_detail"
    ),
    path(
        "reviews/<int:pk>/delete",
        ReviewDeleteView.as_view(),
        name="review_delete"
    ),
    path(
        "reviews/<int:pk>/update/",
        ReviewUpdateView.as_view(),
        name="review_update"
    ),
    path(
        "viewers/<int:pk>/",
        ViewerDetailView.as_view(),
        name="viewer_detail"
    ),
    path(
        "viewers/<int:pk>/update/",
        ViewerUpdateView.as_view(),
        name="viewer_update"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=CustomLoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

]

app_name = "movie_review"
