from django.test.utils import tag
from django.test import TestCase, Client
from django.urls import reverse_lazy
from pytest_django.asserts import assertTemplateUsed

from movie_review_app.models import (
    Movie,
    Review,
    Viewer,
    Comment
)
from movie_review_app.forms import (
    MovieForm, ReviewForm,
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


class MovieViewsTest(TestCase):
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


    def test_movie_list_context_contains(self):
        response = self.client.get("/movies/")

        self.assertIn(
            "is_staff",
            response.context,
        )

    def test_movie_get_queryset(self):
        response = self.client.get(
            "/movies/",
            {"name": "Test name"}
        )

        not_movie_name = "lemefao"
        not_movie = Movie.objects.create(
            name=not_movie_name,
            year=1999,
        )

        self.assertNotContains(response, not_movie.name)

    def test_movie_get_success_url_and_form_udp(self):
        url = reverse_lazy(
            "movie_review:movie_update",
            kwargs={"pk": self.movie.pk}
        )
        response = self.client.post(
            url,
            data={
                "name": "Rename",
                "year": 2020,
            }
        )
        expected_url = reverse_lazy(
                "movie_review:movie_detail",
                kwargs={"pk": self.movie.pk}
            )

        self.assertRedirects(response, expected_url)

    def test_movie_delete_redirect(self):
        url = reverse_lazy(
            "movie_review:movie_delete",
            kwargs={"pk": self.movie.pk}
        )
        response = self.client.post(url)

        self.assertRedirects(response, "/movies/")

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

    def test_movie_not_moderator(self):
        url = reverse_lazy(
            "movie_review:movie_create"
        )
        response = self.client.get(url)

        self.assertContains(
            response,
            "You are not a moderator",
        )


class ReviewsTest(TestCase):
    def setUp(self):
        self.user = Viewer.objects.create_user(
            username="regular_user",
            password="password",
        )
        self.client.force_login(self.user)

        self.movie = Movie.objects.create(
            name="Test name",
            year=1999,
        )

        self.review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.user,
            movie=self.movie,
            rating=5,
        )

    def test_review_list_template(self):
        response = self.client.get("/reviews/")
        self.assertTemplateUsed(response, "movie_review/review_list.html")

    def test_review_detail_context(self):
        url = reverse_lazy(
            "movie_review:review_detail",
            kwargs={"pk": self.review.pk}
        )

        response = self.client.get(url)

        self.assertIn(
            "is_author",
            response.context,
        )

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

    def test_review_update_success_url(self):
        url = reverse_lazy(
            "movie_review:review_update",
            kwargs={"pk": self.review.pk}
        )
        response = self.client.post(
            url,
            data={
                "title": "Rename",
                "content": self.review.content,
                "author": self.review.author.pk,
                "movie": self.review.movie.pk,
                "rating": self.review.rating,
            },
        )
        expected_url = reverse_lazy(
            "movie_review:review_detail",
            kwargs={"pk": self.review.pk}
        )

        self.assertRedirects(response, expected_url)


class NotLoggedInTest(TestCase):
    def setUp(self):
        self.user = Viewer.objects.create_user(
            username="regular_user",
            password="password",
        )

        self.movie = Movie.objects.create(
            name="Test name",
            year=1999,
        )

        self.review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.user,
            movie=self.movie,
            rating=5,
        )

    def test_review_detail_not_logged_in(self):
        url = reverse_lazy(
            "movie_review:review_detail",
            kwargs={"pk": self.review.pk}
        )

        response = self.client.get(url)

        self.assertIn("/login/", response.url)
