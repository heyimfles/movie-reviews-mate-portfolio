from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from movie_review_app.models import (
    Movie,
    Viewer,
    Review,
    Comment,
)


admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)


@admin.register(Viewer)
class ViewerAdmin(UserAdmin):
    pass
