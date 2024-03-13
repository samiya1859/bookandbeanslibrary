from django import forms
from .models import Book,Review

class BookForm(forms.Form):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'review']