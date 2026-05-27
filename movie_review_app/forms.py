from django.contrib.auth.forms import AuthenticationForm
from django import forms

from movie_review_app.models import (
    Review,
    Movie,
    Viewer,
    Comment,
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


class ViewerForm(forms.ModelForm):

    class Meta:
        model = Viewer
        fields = [
            "favourite_movie",
            "first_name",
            "last_name",
        ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            "content",
        )
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "blah blah blah...",
                "rows": 4,
            })
        }


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "placeholder": "cool name",
            "class": "form-control",
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "secret password",
            "class": "form-control",
        })
    )


class MovieSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search for a movie...",
            }
        ),
        label="",
    )
