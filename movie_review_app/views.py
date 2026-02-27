from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from movie_review_app.models import (
    Movie,
    Review,
)


def index(request):
    """
    Main Page view function
    """
    num_movies = Movie.objects.count()
    num_reviews = Review.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session["num_visits"] = num_visits + 1

    last_three_movies = Movie.objects.order_by("-created_at")[:3]
    last_three_reviews = Review.objects.order_by("-created_at")[:3]

    context = {
        "num_movies": num_movies,
        "num_reviews": num_reviews,
        "num_visits": num_visits,
        "last_three_movies": last_three_movies,
        "last_three_reviews": last_three_reviews,
    }

    return render(request, "movie_review/index.html", context)


class MovieListView(generic.ListView):
    model = Movie
    context_object_name = "movie_list"
    template_name = "movie_review/movie_list.html"
    paginate_by = 10


class MovieCreateView(generic.CreateView):
    model = Movie
    fields = "__all__"
    success_url = reverse_lazy("movie_review:movie_list")
    template_name = "movie_review/movie_form.html"


class ReviewListView(generic.ListView):
    model = Review
    context_object_name = "review_list"
    template_name = "movie_review/review_list.html"
    paginate_by = 5


class ReviewCreateView(generic.CreateView):
    model = Review
    fields = "__all__"
    success_url = reverse_lazy("movie_review:review_list")
    template_name = "movie_review/review_form.html"
