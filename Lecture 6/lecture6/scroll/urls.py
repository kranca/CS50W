from django.urls import path

from . import views

app_name = 'scroll'

urlpatterns = [
    path("", views.index, name="index"),
    path("scroll", views.scroll, name="scroll"),
    path("posts", views.posts, name="posts"),
    path("hide", views.hide, name="hide")
]