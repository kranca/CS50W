from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting/", views.create_new_listing_view, name="create_new_listing_view"),
    path("mylistings", views.my_listings, name="my_listings"),
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("category/<str:category_key>/", views.category_view, name="category_view"),
    path("<int:listing_id>", views.listing_view, name="listing_view")
]
