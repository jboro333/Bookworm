from django.conf.urls import url
from books.views import *

urlpatterns = [
    url(r'^home/', home),
    url(r'^search/', search),
    url(r'^add/genre/', CreateGenre.as_view()),
    url(r'^review/book=(?P<book_id>\d+)/', seeReviews),  # Does not work with ? ??
    url(r'^add/review?book=(?P<book_id>\d+)/', createReview),
    url(r'^add/vote?book=(?P<book_id>\d+)&genre=(?P<genre_id>\d+)/', voteGenre),
    url(r'^add/vote?book=(?P<book_id>\d+)/', voteNewGenre),
    url(r'^[a-z]*', notExists)
]