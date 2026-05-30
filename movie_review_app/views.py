from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from movie_review_app.forms import (
    ReviewForm,
    MovieForm,
    ViewerForm,
    CommentForm,
    MovieSearchForm
)
from movie_review_app.models import (
    Movie,
    Review,
    Viewer, Comment,
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

    for movie in last_three_movies:
        if movie.reviews.exists():
            movie.update_avg()

    return render(request, "movie_review/index.html", context)


class MovieListView(LoginRequiredMixin, generic.ListView):
    model = Movie
    context_object_name = "movie_list"
    template_name = "movie_review/movie_list.html"
    paginate_by = 3
    queryset = Movie.objects.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_staff"] = (
                self.request.user.is_staff or
                self.request.user.is_superuser
        )
        context["search_form"] = MovieSearchForm()
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return self.queryset.filter(name__icontains=name)
        else:
            return self.queryset


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
        return (
            reverse_lazy(
                "movie_review:movie_detail",
                kwargs={"pk": movie_id}
            )
        )


class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Movie
    template_name = "movie_review/movie_confirm_delete.html"
    success_url = reverse_lazy("movie_review:movie_list")


class ReviewListView(LoginRequiredMixin, generic.ListView):
    model = Review
    context_object_name = "review_list"
    template_name = "movie_review/review_list.html"
    paginate_by = 3


class ReviewDetailView(LoginRequiredMixin, generic.DetailView):
    model = Review
    template_name = "movie_review/review_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        is_author = (
                self.request.user.is_authenticated and
                (review.author == self.request.user)
        )
        context["is_author"] = is_author
        context["form"] = kwargs.get(
            "form",
            CommentForm,
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                content=form.cleaned_data["content"],
                author=self.request.user,
                review=self.object,
            )
            return redirect("movie_review:review_detail", pk=self.object.id)

        return self.render_to_response(self.get_context_data(**kwargs))


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ReviewForm
    success_url = reverse_lazy("movie_review:review_list")
    template_name = "movie_review/review_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review
    template_name = "movie_review/review_confirm_delete.html"
    success_url = reverse_lazy("movie_review:review_list")


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "movie_review/review_form.html"

    def get_success_url(self):
        review_id = self.object.id
        return reverse_lazy(
            "movie_review:review_detail",
            kwargs={"pk": review_id}
        )


class ViewerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Viewer
    template_name = "movie_review/viewer_detail.html"

    def post(self, request, *args, **kwargs):
        viewer = self.object
        if viewer != request.user:
            raise PermissionDenied


class ViewerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Viewer
    form_class = ViewerForm
    template_name = "movie_review/viewer_form.html"

    def get_success_url(self):
        viewer_id = self.object.id
        return reverse_lazy(
            "movie_review:viewer_detail",
            kwargs={"pk": viewer_id}
        )
