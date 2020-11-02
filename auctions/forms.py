from django import forms
from .models import Listing
from django.forms import ModelForm, Textarea, Select, TextInput, NumberInput


class listing_form(forms.ModelForm):
    class Meta:
        model  = Listing
        fields = ('title', 'category','description', 'image_url', 'initial_bid')
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control mb-2', 'placeholder': 'Title'
            }),
            'category': Select(choices=Listing.categories, attrs={
                'class': 'form-control', 'id': 'inputGroupSelect'
            }),
            'initial_bid': NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Initial Bid'
            }),
            'description': Textarea(attrs={
                'class': 'form-control mb-2', 'placeholder': 'Description'
            }),
            'image_url': TextInput(attrs={
                'class': 'form-control mb-2', 'placeholder': 'Image URL'
            })
        }

        
