from django import forms
from .models import Product, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','slug', 'image', 'description', 'price', 'stock',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text',)
