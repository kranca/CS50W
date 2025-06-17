from django.contrib import admin
from django import forms

from .models import *

# Register your models here.
class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ListingAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Exclude the owner from watchers queryset
            self.fields['watchers'].queryset = User.objects.exclude(pk=self.instance.owner_id)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "last_name", "first_name")

class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm
    list_display = ("id", "object_name", "category", "is_active")
    filter_horizontal = ("watchers",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "offer")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "text")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)