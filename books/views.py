# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Genre, Book, BookScore, GenreScore, Part
from forms import SearchForm, ReviewForm


def buildResult(found, user):
    result = {}
    for book in found:
        # Get series
        series = Part.objects.filter(book=book)
        if (series.count() == 0):
            series = []
        else:
            series = series[0]
            
        # Get genres
        genres = book.best_genres()
        bookGenres = []
        for genre in genres:
            query = GenreScore.objects.filter(user=user, book=book, genre=genre[0])
            bookGenres += [(genre[1], genre[0], query.count() != 0)]
            result[book] = (bookGenres, series)
    return result


# Create your views here.
def home(request):
    if (request.user.is_anonymous):
        return redirect('/login/')
    reviews = BookScore.objects.filter(user=request.user)
    genres = Genre.objects.filter(user=request.user)
    return render(request, 'books/base.html', {'reviews': reviews, 'genres': genres, 'next': '/bookworm/home/'})


def search(request):
    if (request.method == 'POST'):
        form = SearchForm(request.POST)
        if (form.is_valid()):
            fields = form.cleaned_data
            query = ""
            if (fields['title'] != ''):
                query += "book=" + fields['title'] + "&"
            if (fields['author'] != ''):
                query += "author=" + fields['author'] + "&"
            if (fields['series'] != ''):
                query += "series=" + fields['series'] + "&"
            if (fields['editor'] != ''):
                query += "editor=" + fields['editor']
            return redirect('/bookworm/search?' + query)
            
    else:
        book = request.GET.get('book', '')
        author = request.GET.get('author', '')
        series = request.GET.get('series', '')
        editor = request.GET.get('editor', '')
        if (book == '' and author == '' and series == '' and editor == ''):  # Query is empty
            return render(request, 'books/form.html', {'form': SearchForm()})
        
        books = Book.objects.all()
        if (book != ''):
            books = books.filter(title__contains=book)
        if (author != ''):
            books = books.filter(author__name__contains=author)
        if (editor != ''):
            books = books.filter(editor__name__contains=editor)
        if (series != ''):
            parts = Part.objects.filter(series__name__contains=series)
            found = []
            for book in books:
                for part in parts:
                    if (book == part.book):
                        found += [book]
        else:
            found = books
            
        if (found.count() == 0):
            # found = <API search>
        result = buildResult(found, request.user)
        
        query = ""
        for field in request.GET:
            query += field + "=" + request.GET[field] + "&"
        
        return render(request, 'books/queryResult.html', {'result': result, 'next': '/bookworm/search?' + query})
    

class CreateGenre(CreateView):
    model = Genre
    fields = ['name', 'description']
    template_name = "books/form.html"
    success_url = "/bookworm/home/"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateGenre, self).form_valid(form)


class DeleteGenre(DeleteView):
    model = Genre
    success_url = "/bookworm/home/"
    template_name = "books/confirmation.html"
    
    def get_object(self, queryset=None):
        instance = super(DeleteGenre, self).get_object()
        if (instance.user != self.request.user):
            raise Http404
        return instance


class CreateReview(CreateView):
    model = BookScore
    fields = ['title', 'score', 'text']
    template_name = "books/form.html"  # Previous url
    success_url = "/bookworm/home/"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = Book.objects.filter(id=self.kwargs['pk'])[0]
        return super(CreateView, self).form_valid(form)


class ModifyReview(UpdateView):
    model = BookScore
    success_url = "/bookworm/home/"  # Previous url
    template_name = "books/form.html"
    fields = ['title', 'score', 'text']
    
    def get_object(self, queryset=None):
        instance = super(UpdateView, self).get_object()
        if (instance.user != self.request.user):
            raise Http404
        return instance


class DeleteReview(DeleteView):
    model = BookScore
    success_url = "/bookworm/home/"
    template_name = "books/confirmation.html"
    
    def get_object(self, queryset=None):
        instance = super(DeleteView, self).get_object()
        if (instance.user != self.request.user):
            raise Http404
        return instance


def voteTopGenre(request, book_pk, genre_pk):
    book = Book.objects.filter(id=book_pk)[0]
    genre = Genre.objects.filter(id=genre_pk)[0]    
    vote, created = GenreScore.objects.get_or_create(book=book, user=request.user, genre=genre)
    if (not created):
        vote.delete()
    return redirect(request.POST['next'])


def voteNewGenre(request, book_id):
    pass        


def seeBook(request, pk):
    book = Book.objects.filter(id=pk)[0]
    series = Part.objects.filter(book__id=pk)
    if (series.count() == 0):
        series = None
    else:
        series = series[0]
    
    genreQuery = book.best_genres()
    genres = []
    for genre, votes in genreQuery:
        vote = GenreScore.objects.filter(genre=genre, book=book, user=request.user)
        genres += [(genre, votes, vote.count() != 0)]
        
    return render(request, 'books/book.html', {'book': book, 'series': series, 'genres': genres})


def seeReviews(request, pk):
    reviews = BookScore.objects.filter(book__id=pk)
    book = Book.objects.filter(id=pk)[0]
    return render(request, 'books/reviews.html', {'book': book, 'reviews':[review for review in reviews]})


def notExists(request):
    raise Http404("Page not found")
