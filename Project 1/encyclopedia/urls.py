from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.get_entry, name="get_entry"),
    path("search/", views.search_entry, name= "search_entry"),
]
