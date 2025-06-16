from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing/", views.create_new_listing_view, name="create_new_listing_view"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("<str:listing_id>", views.listing_view, name="listing_view")
]
