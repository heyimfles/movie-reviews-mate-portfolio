from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from pytest_django.asserts import assertTemplateUsed

from movie_review_app.models import (
    Movie,
    Review,
    Viewer,
    Comment
)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_correct_response(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_index_navbar_present(self):
        response = self.client.get("")
        assertTemplateUsed(response, "includes/navbar.html")

    def test_index_correct_template(self):
        response = self.client.get("")
        assertTemplateUsed(response, "movie_review/index.html")


class MovieViewsRegularTest(TestCase):
    def setUp(self):
        self.regular_user = Viewer.objects.create_user(
            username="regular_user",
            password="password",
        )
        self.client.force_login(self.regular_user)

        self.movie = Movie.objects.create(
            name="Test name",
            year=1999,
        )

        self.positive_review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.regular_user,
            movie=self.movie,
            rating=5,
        )

        self.negative_review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.regular_user,
            movie=self.movie,
            rating=1,
        )


    def test_movie_list_context_contains(self):
        response = self.client.get("/movies/")

        self.assertIn(
            "is_staff",
            response.context,
        )

    def test_movie_get_queryset(self):
        response = self.client.get("/movies/")


