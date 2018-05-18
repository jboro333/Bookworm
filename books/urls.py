from django.conf.urls import url
from books.views import *

urlpatterns = [
    url(r'^home/', home),  # Home page
    url(r'^search?', search),  # Search bookworm
    url(r'^add/genre/', CreateGenre.as_view()),  # Add new genre
    url(r'^review?', seeReviews),  # See the reviews for a book
    url(r'^add/review?', createReview),  # Create new review for a book
    url(r'^add/vote?', voteGenre),  # Vote a genre
    url(r'^[a-z]*', notExists)
]