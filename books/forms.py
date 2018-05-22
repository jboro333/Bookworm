from django import forms
from models import BookScore

class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    author = forms.CharField(max_length=50, required=False)
    series = forms.CharField(max_length=50, required=False)
    editor = forms.CharField(max_length=50, required=False)
    
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = BookScore
        fields = ['title', 'score', 'text']
        template_name = "books/form.html"
    
    