from crispy_forms.helper import FormHelper
from django import forms

from movie_review_app.models import (
    Review,
    Movie,
)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "name",
            "year",
        ]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "movie",
            "rating",
        ]
