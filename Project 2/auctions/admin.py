from django.contrib import admin

from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "last_name", "first_name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "object_name", "category", "is_active")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "offer")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "text")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)