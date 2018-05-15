from django import forms
from models import BookScore

class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    author = forms.CharField(max_length=50, required=False)
    
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = BookScore
        fields = ['score', 'text']
        template_name = "books/form.html"
    
    