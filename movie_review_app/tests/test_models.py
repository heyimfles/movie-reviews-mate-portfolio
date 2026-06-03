from django.test import TestCase
from unittest import mock

from movie_review_app.models import (
    Movie,
    Review,
    Viewer,
    Comment
)


class ModelsTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="Test name",
            year=1999,
        )

        self.viewer = Viewer.objects.create_user(
            username="coolusername",
            password="password",
            favourite_movie=self.movie,
        )

        self.positive_review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.viewer,
            movie=self.movie,
            rating=5,
        )

        self.negative_review = Review.objects.create(
            title="Test review",
            content="Test content",
            author=self.viewer,
            movie=self.movie,
            rating=1,
        )

        self.comment = Comment.objects.create(
            content="Test comment",
            author=self.viewer,
            review=self.positive_review,
        )

    def test_movie_upd_avg(self):
        all_ratings = [
            review.rating for
            review in
            self.movie.reviews.all()
        ]
        avg = sum(all_ratings) / len(all_ratings)
        self.assertEqual(self.movie.avg_rating, avg)

    def test_review_function_called_on_save(self):
        with mock.patch(
                "movie_review_app.models.Movie.update_avg"
        ) as mock_update_avg:
            review = Review.objects.create(
                title="Test review",
                content="Test content",
                author=self.viewer,
                movie=self.movie,
                rating=5,
            )
            mock_update_avg.assert_called_once()

    def test_review_function_called_on_delete(self):
        with mock.patch(
                "movie_review_app.models.Movie.update_avg"
        ) as mock_update_avg:
            self.positive_review.delete()
            mock_update_avg.assert_called_once()

    def test_movie_string(self):
        self.assertEqual(
            str(self.movie),
            f"{self.movie.name} ({self.movie.year})"
        )

    def test_viewer_string(self):
        self.assertEqual(
            str(self.viewer),
            f"{self.viewer.username} "
            f"({self.viewer.first_name} "
            f"{self.viewer.last_name})"
        )

    def test_review_string(self):
        self.assertEqual(
            str(self.positive_review),
            f"Review for {self.movie.name} "
            f"by {self.positive_review.author} with "
            f"rating of {self.positive_review.rating}"
        )

    def test_comment_string(self):
        self.assertEqual(
            str(self.comment),
            f"Comment for {self.comment.review} " 
            f"by {self.comment.author}"
        )
