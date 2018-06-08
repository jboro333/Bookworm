from behave import *

use_step_matcher("parse")

@given(u'A book "{book}" by author "{author}"')
def step_impl(context, book, author):
    from books.models import Book, Author
    author = Author.objects.create(name=author, desc="BLABLABLA")
    author.save()
    Book.objects.create(title=book, author=author).save()
