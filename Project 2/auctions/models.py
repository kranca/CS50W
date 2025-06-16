from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    ELECTRONICS = 'EL'
    FASHION = 'FA'
    HOMEGARDEN = 'HG'
    SPORTS = 'SP'
    TOYS = 'TO'
    OTHER = 'OT'

    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (HOMEGARDEN, 'Home & Garden'),
        (SPORTS, 'Sports'),
        (TOYS, 'Toys'),
        (OTHER, 'Other'),
    ]

    object_name = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    starting_bid = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    current_bid = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings_where_user_is_highest_bidder"
    )
    image = models.URLField(blank=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_listings"
    )
    is_active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)

    def __str__(self):
        return f"{self.id}: {self.object_name}, active = {self.is_active}"
    
class Bid(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids_users"
    )
    offer = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.id}: {self.listing.object_name}, offer = {self.offer}"

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.object_name}"

@receiver(post_save, sender=Bid)
def update_listing_current_bid_on_save(sender, instance, **kwargs):
    listing = instance.listing
    highest_bid = listing.bids.order_by('-offer').first()
    if highest_bid and highest_bid.offer > listing.starting_bid:
        listing.current_bid = highest_bid.offer
        listing.bidder = highest_bid.user
    else:
        listing.current_bid = None
        listing.bidder = None
    listing.save()

@receiver(post_delete, sender=Bid)
def update_listing_current_bid_on_delete(sender, instance, **kwargs):
    listing = instance.listing
    highest_bid = listing.bids.order_by('-offer').first()
    if highest_bid and highest_bid.offer > listing.starting_bid:
        listing.current_bid = highest_bid.offer
        listing.bidder = highest_bid.user
    else:
        listing.current_bid = None
        listing.bidder = None
    listing.save()