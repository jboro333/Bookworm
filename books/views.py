# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView

from models import Genre, Book, BookScore, GenreScore
from forms import SearchForm, ReviewForm



# Create your views here.
def home(request):
    reviews = BookScore.objects.filter(user=request.user)
    genres = Genre.objects.filter(user=request.user)
    return render(request, 'books/base.html', {'reviews': reviews, 'genres': genres})

def search(request):
    if (request.method == 'POST'):
        form = SearchForm(request.POST)
        if (form.is_valid()):
            fields = form.cleaned_data
            return redirect('/bookworm/search?book=%s&author=%s' % (fields['title'], fields['author']))
            
    else:
        book = request.GET.get('book', '')
        author = request.GET.get('author', '')
        if (book == '' and author == ''):  # Query is empty
            return render(request, 'books/form.html', {'form': SearchForm()})
        
        result = {}
        books = Book.objects.filter(title__contains=book, author__name__contains=author)
        for book in books:
            genres = book.best_genres()
            bookGenres = []
            for genre in genres:
                query = GenreScore.objects.filter(user=request.user, book=book, genre=genre[0])
                bookGenres += [(genre[1], genre[0], query.count() != 0)]
                result[book] = bookGenres
        print result
        
        return render(request, 'books/queryResult.html', {'result': result})
    

class CreateGenre(CreateView):
    model = Genre
    fields = ['name', 'description']
    template_name = "books/form.html"
    success_url = "/bookworm/home/"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateGenre, self).form_valid(form)
    
def createReview(request):
    book_id = request.GET.get('book', '')
    if (book_id == ''):
        return redirect('/bookworm/home')
    if (request.method == 'POST'):
        form = ReviewForm(request.POST)
        if (form.is_valid()):
            fields = form.cleaned_data
            if (fields['score'] >= 0 and fields['score'] <= 10):
                book = Book.objects.filter(id=book_id)[0]
                newReview = BookScore(book=book, user=request.user, score=fields['score'], text=fields['text'])
                newReview.save()
                return redirect('/bookworm/home/')  # Has to redirect to previous page
            
    else:
        form = ReviewForm()
        
    return render(request, 'books/form.html', {'form': form})  

def voteGenre(request):
    if (request.GET.get('genre', '') != ''):
        return voteTopGenre(request, int(request.GET.get('book', '')), int(request.GET.get('genre', '')))
    else:
        return voteNewGenre(request, int(request.GET.get('book', '')))

def voteTopGenre(request, book_id, genre_id):
    book = Book.objects.filter(id=book_id)[0]
    genre = Genre.objects.filter(id=genre_id)[0]    
    vote, created = GenreScore.objects.get_or_create(book=book, user=request.user, genre=genre)
    if (not created):
        vote.delete()
    return redirect('/bookworm/home/')  # Has to redirect to previous page    
    
def voteNewGenre(request, book_id):
    pass        

def seeReviews(request):
    book_id = request.GET.get('book', '')
    if (book_id == ''):
        return redirect('/bookworm/home/')
    reviews = BookScore.objects.filter(book__id=book_id)
    book = Book.objects.filter(id=book_id)[0]
    return render(request, 'books/reviews.html', {'book': book, 'reviews':[review for review in reviews]})

def notExists(request):
    raise Http404("Page not found")
