from behave import *

use_step_matcher("parse")

@given(u'A review for book "{book}"')
def step_impl(context, book):
    from books.models import Book
    book = Book.objects.filter(name=book)[0]
    context.browser.visit('/bookworm/book/' + str(book.id) + '/review/add/')
    for parameter in context.table.headings:
        context.browser.fill(parameter, context.table[parameter])
    context.browser.find_by_tag('form').find_by_value("Submit").click()
    

@when(u'I create review for book {book}')
def step_impl(context, book):
    from books.models import Book
    book = Book.objects.filter(name=book)[0]
    context.browser.visit('/bookworm/book/' + str(book.id) + '/review/add/')
    for parameter in context.table.headings:
        context.browser.fill(parameter, context.table[parameter])
    context.browser.find_by_tag('form').find_by_value("Submit").click()

@when(u'I modify review "{rev}" for book {book}')
def step_impl(context, book, rev):
    from books.models import Book, BookScore
    book = Book.objects.filter(name=book)[0]
    rev = BookScore.objects.filter(name=rev)[0]
    context.browser.visit('/bookworm/book/' + str(book.id) + '/review/ ' + str(rev.id) + '/mod/')
    for parameter in context.table.headings:
        context.browser.fill(parameter, context.table[parameter])
    context.browser.find_by_tag('form').find_by_value("Submit").click()

@when(u'I delete review')
def step_impl(context):
    table = context.table
    context.browser.visit('/bookworm/home')
    link = context.browser.find_by_xpath('/html/body/main/div[1]/div[2]/a[2]')
    link.click()


@then(u'There are {numreviews:n} reviews in my review list')
def step_impl(context, numreviews):
    context.browser.visit('/bookworm/home/')
    divs = context.browser.find_by_xpath('/html/body/main/div')
    assert len(divs) == numreviews


@then(u'The new score for review "{rev}" is {score}')
def step_impl(context, rev, score):
    from models import BookScore
    assert BookScore.objects.filter(name=rev)[0].score == int(score)
