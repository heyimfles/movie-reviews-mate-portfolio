from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class Movie(models.Model):
    """
    This is movie model, it has name, year of publication
    and avg_rating which comes from reviews left by viewers,
    if there are no reviews, default is 0
    """

    name = models.CharField(
        max_length=255,
    )
    year = models.IntegerField(
        blank=True,
        null=True,
    )
    avg_rating = models.FloatField(
        default=0,
    )

    def __str__(self):
        return f"{self.name} ({self.year})"


class Viewer(AbstractUser):
    """
    This is viewer model, or user
    they have unrequired fav_mobie field
    """

    favourite_movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="viewers",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "viewer"
        verbose_name_plural = "viewers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Review(models.Model):
    """
    This is review model, it has title, content, author,
    movie and the rating for it which can be only chosen between written choices
    """
    RATING_CHOICES = [
        (1, "Terrible"),
        (2, "Bad"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent"),
    ]

    title = models.CharField(
        max_length=255,
    )
    content = models.CharField(
        max_length=255,
    )
    author = models.ForeignKey(
        Viewer,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.SmallIntegerField(
        choices=RATING_CHOICES,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Review for {self.movie} "
            f"by {self.author} with"
            f"rating of {self.rating}"
        )


class Comment(models.Model):
    """
    This is comment model, it has content and author
    it also has the creation time and review to which it is linked
    """

    content = models.CharField(
        max_length=255,
    )
    author = models.ForeignKey(
        Viewer,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment for {self.review}" f"by {self.author}"
