from django import forms
from models import Genre

class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    author = forms.CharField(max_length=50, required=False)
    series = forms.CharField(max_length=50, required=False)
    editor = forms.CharField(max_length=50, required=False)
    
class GenreForm(forms.Form):
    name = forms.CharField(label='Genre', max_length=50)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if (Genre.objects.filter(name=name).count() == 0):
            raise forms.ValidationError('Genre does not exist')
        return name

    class Meta:
        template_name = "books/form.html"
    
    