from django.test import TestCase
from django.urls import reverse_lazy
from pytest_django.asserts import assertTemplateUsed

from movie_review_app.models import (
    Movie,
    Review,
    Viewer,
)
from movie_review_app.forms import (
    MovieForm,
    ReviewForm,
    CustomLoginForm,
    MovieSearchForm,
)


class FormTests(TestCase):
    def setUp(self):
        self.password = "password"
        self.user = Viewer.objects.create_user(
            username="user",
            password=self.password,
        )
        self.client.force_login(self.user)

        self.movie_name = "Cool name"
        self.movie = Movie.objects.create(
            name=self.movie_name,
            year=1999,
        )

        self.review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.user,
            movie=self.movie,
            rating=5,
        )

    def test_movie_form_valid(self):
        form_data = {
            "name": "Test name",
            "year": 1999,
        }
        form = MovieForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_movie_form_invalid(self):
        form_data = {
            "name": "Test name",
            "year": 3000,
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_review_form_valid(self):
        form_data = {
            "title": "Test title",
            "content": "Test content",
            "movie": self.movie,
            "rating": 1,
        }

        form = ReviewForm(data=form_data)

        self.assertTrue(form.is_valid())

        def test_review_form_author_cannot_be_changed(self):
            another_user = Viewer.objects.create_user(
                username="another_user",
                password="password",
            )

            bad_review_title = "HACKED_AUTHOR"
            form_data = {
                "title": bad_review_title,
                "content": "Test content",
                "movie": self.movie.pk,
                "rating": 3,
                "author": another_user.pk,
            }

            url = reverse_lazy(
                "movie_review:review_create"
            )

            self.client.post(url, data=form_data)
            review = Review.objects.get(title=bad_review_title)

            self.assertNotEqual(review.author, another_user)

    def test_viewer_form_correct_template(self):
        response = self.client.get(
            reverse_lazy(
                "movie_review:viewer_update",
                kwargs={"pk": self.user.pk},
            )
        )

        self.assertTemplateUsed(
            response,
            "movie_review/viewer_form.html",
        )

    def test_comment_form_correct_template(self):
        response = self.client.get(
            reverse_lazy(
                "movie_review:review_detail",
                kwargs={"pk": self.review.pk},
            )
        )

        self.assertTemplateUsed(
            response,
            "includes/comment_form.html",
        )

    def test_custom_login_form_valid(self):
        form_data = {
            "username": self.user.username,
            "password": self.password,
        }
        form = CustomLoginForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_movie_search_form_valid(self):
        form_data = {
            "name": "name"
        }
        form = MovieSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

