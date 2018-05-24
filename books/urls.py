from django.conf.urls import url
from books.views import *

urlpatterns = [
    url(r'^home/', home),  # Home page
    url(r'^search?', search),  # Search bookworm
    url(r'^book/(?P<book_pk>\d+)/vote/(?P<genre_pk>\d+)/add/', voteTopGenre),  # Vote a top genre
    url(r'^book/(?P<pk>\d+)/vote/add/', voteGenre),  # Vote a genre
    url(r'^book/(?P<pk>\d+)/review/add/', CreateReview.as_view()),  # Create new review for a book
    url(r'^book/(\d+)/review/(?P<pk>\d+)/mod/', ModifyReview.as_view()),  # Change review for a book
    url(r'^book/(\d+)/review/(?P<pk>\d+)/del/', DeleteReview.as_view()),  # Delete review for a book    
    url(r'^book/(?P<pk>\d+)/review/', seeReviews),  # See the reviews for a book    
    url(r'^book/(?P<pk>\d+)/', seeBook),  # View a book
    url(r'^genre/(?P<pk>\d+)/del/', DeleteGenre.as_view()),  # Remove genre
    url(r'^genre/add/', CreateGenre.as_view()),  # Add new genre
    url(r'^author/(?P<pk>\d+)/', seeAuthor),
    # url(r'^[a-z]*', notExists)
]