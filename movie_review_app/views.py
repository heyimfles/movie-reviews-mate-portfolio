from django.shortcuts import render

from movie_review_app.models import Movie, Review


def index(request):
    """
    Main Page view function
    """
    num_movies = Movie.objects.count()
    num_reviews = Review.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_movies": num_movies,
        "num_reviews": num_reviews,
        "num_visits": num_visits
    }

    return render(request, "movie_review/index.html", context)