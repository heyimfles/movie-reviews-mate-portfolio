from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


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
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.name} ({self.year})"

    def update_avg(self):
        agg = self.reviews.aggregate(avg=Avg("rating"))
        self.avg_rating = agg["avg"] or 0
        self.save()

    def format_avg(self):
        return f"{self.avg_rating:.1f}"


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
    movie and the rating for it
    which can be only chosen between written choices
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

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            self.movie.update_avg()

    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_avg()


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
