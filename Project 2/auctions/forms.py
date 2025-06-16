from django import forms
from .models import Listing, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['object_name', 'description', 'starting_bid', 'image', 'category']

    category = forms.ChoiceField(choices=Listing.CATEGORY_CHOICES)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'text': '',
        }