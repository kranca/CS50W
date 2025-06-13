from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello", views.hello, name="hello"),
    path("counter", views.counter, name="counter"),
    path("color", views.color, name="color"),
    path("color/selector", views.color_selector, name="color_selector"),
    path("tasks", views.tasks, name="tasks"),
    path("currency", views.currency, name="currency"),
    path('exchange_rates/', views.exchange_rates, name='exchange_rates_api'),
]