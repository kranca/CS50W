from django.urls import path

from . import views

app_name = 'react'

urlpatterns = [
    path("", views.index, name="index"),
    path("counter", views.counter, name="counter"),
    path("addition", views.addition, name="addition"),
]