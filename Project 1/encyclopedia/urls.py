from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.get_entry, name="get_entry"),
    path("search/", views.search_entry, name= "search_entry"),
    path("random/", views.get_random_entry, name="get_random_entry"),
    path("new_page/", views.new_page, name="new_page"),
    path("<str:entry>/edit", views.edit_page, name="edit_page")
]
