# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2
import bs4

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError

from models import Genre, Book, BookScore, GenreScore, Part, Author, Series
from forms import SearchForm, GenreForm

def getBookInfo(data):
    if ("#" in data):
        title = data.split('(')[0].rstrip()
    
        # Get series and number
        if ("#" in data and "(" in data and ")" in data):
            partInfo = data.split('(')[1].rstrip(')').split("#")
            try:
                return (title, partInfo[0].strip(), int(partInfo[1].strip()))
            except:
                return (None, None, None)
    return (data, None, None)


def getAuthor(author):
    name = author.find("name").text
    query = ""
    for letter in name:
        if (letter.isalpha() or letter == " "):
            query += letter
    # Webscrap
    authorString = "https://www.goodreads.com/author/show/%s.%s" % (author.find("id").text, query)
    handler = urllib2.urlopen(authorString)
    text = handler.read()
    handler.close()
    soup = bs4.BeautifulSoup(text, "lxml")
    desc = ""
    search = soup.find('span', id="freeTextauthor" + author.find("id").text)
    if (search is None):
        search = soup.find('span', id="freeTextContainerauthor" + author.find("id").text)
    for span in search.strings:
        if ("There is more than one author in the Goodreads database with this name" in span):
            continue
        desc += span + "\n"
    return Author.objects.create(name=author.find("name").text, desc=desc)
    

def searchInApi(query):
    queryString = "http://www.goodreads.com/search/index.xml?key=BkZAa7iQldcYvPHCoBZgw&q="  # External config file
    # Create query string
    if ('book' in query):
        queryString += query['book']
    if ('author' in query):
        queryString += query['author']
    if ('' in query):
        queryString += query['']
    queryString = "%20".join(queryString.split())

    # Search books in API
    handler = urllib2.urlopen(queryString)
    text = handler.read()
    handler.close()
    soup = bs4.BeautifulSoup(text, "lxml")
    occurrences = soup.find("search").find("results").find_all("work")
    
    # Add best results
    books = []
    for event in occurrences:
        book = event.find("best_book")
        author = event.find("author")
        authorInDb = Author.objects.filter(name=author.find("name").text)
        if (authorInDb.count() == 0):
            authorInDb = getAuthor(author)
            authorInDb.save()
            print("Created new author: " + author.find("name").text)
        else:
            authorInDb = authorInDb[0]
            
        # Add book to the database
        (title, seriesName, number) = getBookInfo(book.find("title").text)
        if (not title):
            continue
        book = Book.objects.create(title=title, author=authorInDb)
        book.save()
        print("Added book to database: " + title)
        books.append(book)
        
        if (seriesName):
            series = Series.objects.filter(name=seriesName)
            # Add series if it doesn't exist
            if (series.count() == 0):
                series = [Series.objects.create(name=seriesName)]
                series[0].save()
            Part.objects.create(book=book, series=series[0], number=number).save()
    return books
    
    
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
        fields = {}
        if (book != ''):
            books = books.filter(title__contains=book)
            fields['book'] = book
        if (author != ''):
            books = books.filter(author__name__contains=author)
            fields['author'] = author
        if (editor != ''):
            books = books.filter(editor__name__contains=editor)
            fields['editor'] = editor
        if (series != ''):
            parts = Part.objects.filter(series__name__contains=series)
            fields['series'] = series
            found = []
            for book in books:
                for part in parts:
                    if (book == part.book):
                        found += [book]
        else:
            found = [book for book in books]
        print "Found in database:", found
            
        if (found == []):
            found = searchInApi(fields)
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
        mark = form.cleaned_data['score']
        try:
            mark = int(mark)
        except:
            raise ValidationError("Score has to be between 0 and 10")
        if (mark < 0 or mark > 10):
            raise ValidationError("Score has to be between 0 and 10")
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
    
    def form_valid(self, form):
        mark = form.cleaned_data['score']
        try:
            mark = int(mark)
        except:
            raise ValidationError("Score has to be between 0 and 10")
        if (mark < 0 or mark > 10):
            raise ValidationError("Score has to be between 0 and 10")
        return super(UpdateView, self).form_valid(form)    


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


def voteGenre(request, pk):
    if (request.method == 'GET'):
        form = GenreForm()
        print request.GET
    else:
        form = GenreForm(request.POST)
        if (form.is_valid() or form.errors == {'name': ['Genre with this Name already exists.']}):
            genreName = form.cleaned_data['name']
            genre = Genre.objects.filter(name=genreName)
            if (genre.count() == 0):
                raise ValidationError("Genre does not exist")
            GenreScore.objects.create(book=Book.objects.filter(id=pk)[0], genre=genre[0], user=request.user).save()
            return redirect(request.POST['next'])
    genres = [genre.unicode().encode('utf8') for genre in Genre.objects.all()]
    return render(request, 'books/form.html', {'pk': pk, 'genres': genres, 'form': form, 'next': request.GET['next']})
            


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


def seeAuthor(request, pk):
    author = Author.objects.filter(id=pk)[0]
    return render(request, 'books/author.html', {'author': author})


def notExists(request):
    raise Http404("Page not found")
