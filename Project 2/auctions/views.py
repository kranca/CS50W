from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import CommentForm, ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
                )
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comment_form = CommentForm()

    if request.user in listing.watchers.all():
        is_in_watchlist = True
    else:
        is_in_watchlist = False

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "bid":
            bid_value = float(request.POST["bid_value"])
            current = listing.current_bid or listing.starting_bid
            if bid_value > (listing.current_bid or listing.starting_bid):
                Bid.objects.create(
                    listing=listing,
                    user=request.user,
                    offer=bid_value
                )
                messages.success(request, "Your bid was placed successfully.")
            else:
                messages.error(request, f"Your bid must be higher than the current bid (${current:.2f}).")

        elif action == "close" and request.user == listing.owner:
            listing.is_active = False
            listing.save()
            messages.success(request, "Listing has been closed.")
        
        elif action == "comment_submit" and request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
        
        elif action == "add_watchlist" and request.user.is_authenticated:
            listing.watchers.add(request.user)
            listing.save()

        elif action == "remove_watchlist" and request.user.is_authenticated:
            listing.watchers.remove(request.user)
            listing.save()
        
        return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "bids" : listing.bids.order_by("-offer"),
        "comment_form" : comment_form,
        "is_in_watchlist" : is_in_watchlist
    })

@login_required
def create_new_listing_view(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listing_view', listing_id=listing.id)
    else:
        form = ListingForm()

    return render(request, "auctions/new_listing.html", {
        "form": form
    })

@login_required
def my_listings(request):
    all_listings = Listing.objects.filter(owner=request.user)
    active_listings = all_listings.filter(is_active=True)
    closed_listings = all_listings.filter(is_active=False)
    return render(request, "auctions/my_listings.html", {
        "active_listings": active_listings,
        "closed_listings": closed_listings
    })

@login_required
def my_watchlist(request):
    user_watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist
    })