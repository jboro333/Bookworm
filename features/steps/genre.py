from behave import *

use_step_matcher("parse")

@given(u'A genre named "{genre}"')
def step_impl(context, genre):
    from models import Genre
    Genre.objects.create(name=genre, desc="BLABLABLA").save()
    
@given(u'A vote by "{user}" of "{genre}" on "{book}"')
def step_impl(context, book, genre, user):
    from django.contrib.auth.models import User
    from models import GenreScore
    GenreScore.objects.create(genre=Genre.objects.filter(name=genre)[0],
                              book=Book.objects.filter(title=book)[0],
                              user=User.objects.filter(username=user)[0])

    
@when(u'I create genre')
def step_impl(context):
    context.browser.visit('/bookworm/genre/add/')
    context.browser.fill(context.table.headings[0], context.table[context.table.headings[0]])
    context.browser.find_by_tag('form').find_by_value("Submit").click()

@when(u'I vote or devote genre "{genre}" in book "{book}"')
def step_impl(context, book, genre):
    from models import Book, Genre
    book_pk = Book.objects.filter(title=book)[0].id
    book_pk = Genre.objects.filter(name=genre)[0].id
    context.browser.visit('/bookworm/book/' + book_pk + '/vote/' + genre_pk)


@then(u'There are {numgenres:n} genres in my genre list')
def step_impl(context, numgenres):
    context.browser.visit('/bookworm/home/')
    divs = context.browser.find_by_xpath('/html/body/main/div')
    assert len(divs) == numgenres
    
@then(u'Then "{genre}" has {votes:n} votes in "{book}"')
def step_impl(context, genre, book, votes):
    from models import GenreScore
    assert GenreScore.objects.filter(book__title=book, genre__name=genre).count() == int(votes)