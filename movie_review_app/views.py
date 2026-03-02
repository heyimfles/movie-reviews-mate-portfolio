from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from movie_review_app.forms import ReviewForm, MovieForm
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


class MovieListView(LoginRequiredMixin, generic.ListView):
    model = Movie
    context_object_name = "movie_list"
    template_name = "movie_review/movie_list.html"
    paginate_by = 10


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy("movie_review:movie_list")
    template_name = "movie_review/movie_form.html"


class MovieDetailView(LoginRequiredMixin, generic.DetailView):
    model = Movie
    template_name = "movie_review/movie_detail.html"


class MovieUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "movie_review/movie_form.html"

    def get_success_url(self):
        movie_id = self.object.id
        return reverse_lazy("movie_review:movie_detail", kwargs={"pk": movie_id})


class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Movie
    template_name = "movie_review/movie_confirm_delete.html"
    success_url = reverse_lazy("movie_review:movie_list")


class ReviewListView(LoginRequiredMixin, generic.ListView):
    model = Review
    context_object_name = "review_list"
    template_name = "movie_review/review_list.html"
    paginate_by = 5


class ReviewDetailView(LoginRequiredMixin, generic.DetailView):
    model = Review
    template_name = "movie_review/review_detail.html"


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ReviewForm
    success_url = reverse_lazy("movie_review:review_list")
    template_name = "movie_review/review_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

