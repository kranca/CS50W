from django.urls import path

from . import views

app_name = 'animate'

urlpatterns = [
    path("", views.index, name="index"),
]