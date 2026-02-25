from django.contrib import admin

from movie_review_app.models import (
    Movie,
    Viewer,
    Review,
    Comment,
)


admin.site.register(Movie)
admin.site.register(Viewer)
admin.site.register(Review)
admin.site.register(Comment)
